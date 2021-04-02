import re
from datetime import date
from functools import lru_cache
from typing import NamedTuple

from ochs.builder.page import Page
from ochs.builder.templates import get_template
from ochs.builder.variables import apply_global_variables
from ochs.utils import log
from ochs.utils.fs import read_md, read_yaml, write


class PostSpec(NamedTuple):
    name: str
    template: str
    title: str
    author: str
    date: date
    url: str


class Post(NamedTuple):
    spec: PostSpec
    preview: str
    content: str


@lru_cache(maxsize=None)
def load_specs(source_dir: str) -> list[PostSpec]:
    specs = [
        PostSpec(
            name=raw_spec["post"],
            template=raw_spec["template"],
            title=raw_spec["title"],
            author=raw_spec["author"],
            date=date.fromisoformat(raw_spec["date"]),
            url=raw_spec["url"],
        )
        for raw_spec in read_yaml(f"{source_dir}/posts.yaml")
    ]

    return sorted(specs, key=lambda spec: spec.date, reverse=True)


@lru_cache(maxsize=None)
def load_post(spec: PostSpec, source_dir: str) -> Post:
    log.info(f"Reading post '{spec.name}.md'.")
    return Post(
        spec=spec,
        preview=read_md(f"{source_dir}/previews/{spec.name}.md"),
        content=read_md(f"{source_dir}/posts/{spec.name}.md"),
    )


def get_page(post: Post, source_dir: str) -> Page:
    content = get_template(source_dir, post.spec.template)
    content = apply_global_variables(content, source_dir)
    content = apply_post_variables(content, post)
    return Page(url=f"posts/{post.spec.url}", content=content)


def expand_post_block(content: str, source_dir: str) -> str:
    # Determine where block starts and ends
    start_location = content.find("#{post-start}")
    end_location = content.find("#{post-end}") + len("#{post-end}")
    if start_location == -1 or end_location == -1:
        return content

    # Separate content above and below block for later use
    content_above_block = content[:start_location]
    content_below_block = content[end_location:]

    raw_block = content[start_location:end_location]
    block_lines = raw_block.splitlines()

    # Get repeat count and block without stard/end delimiters
    count = int(re.findall("[0-9]+", block_lines[0])[0])
    block = "\n".join(block_lines[1:-1])

    # Create expanded content
    expanded_content = content_above_block
    for spec in load_specs(source_dir)[:count]:
        post = load_post(spec, source_dir)
        expanded_content += apply_post_variables(block, post)
    expanded_content += content_below_block

    return expanded_content


def apply_post_variables(content: str, post: Post) -> str:
    date_instances = set(re.findall(r"#{post-date:[^}]+}", content))
    for date_instance in date_instances:
        date_format = date_instance[12:-1]
        content = content.replace(date_instance, post.spec.date.strftime(date_format))

    return (
        content.replace("#{post-title}", post.spec.title)
        .replace("#{post-author}", post.spec.author)
        .replace("#{post-url}", post.spec.url)
        .replace("#{post-preview}", post.preview)
        .replace("#{post-content}", post.content)
    )


def build_posts(source_dir: str, target_dir: str) -> None:
    specs = load_specs(source_dir)
    posts = [load_post(spec, source_dir) for spec in specs]
    pages = [get_page(post, source_dir) for post in posts]

    for page in pages:
        page.write(target_dir)
