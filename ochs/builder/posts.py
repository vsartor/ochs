import re
from datetime import date
from functools import lru_cache
from typing import NamedTuple

from ochs.builder.templates import get_template
from ochs.builder.variables import apply_global_variables
from ochs.utils.fs import read_md, read_yaml, write
from ochs.utils.logging import logger
from ochs.utils.term import bold


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


class PostPage(NamedTuple):
    url: str
    content: str


@lru_cache(maxsize=None)
def load_specs(source_dir: str) -> list[PostSpec]:
    return [
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


def load_post(spec: PostSpec, source_dir: str) -> Post:
    logger().info(f"Reading post '{bold(spec.name)}.md'.")
    return Post(
        spec=spec,
        preview=read_md(f"{source_dir}/previews/{spec.name}.md"),
        content=read_md(f"{source_dir}/posts/{spec.name}.md"),
    )


def load_post_page(post: Post, source_dir: str) -> PostPage:
    content = get_template(source_dir, post.spec.template)
    content = apply_global_variables(content, source_dir)
    content = apply_post_variables(content, post)
    return PostPage(url=post.spec.url, content=content)


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
    pages = [load_post_page(post, source_dir) for post in posts]

    for page in pages:
        logger().info(f"Writing post page '{bold(page.url)}'.")
        write(f"{target_dir}/posts/{page.url}", page.content)
