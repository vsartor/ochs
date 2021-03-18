import setuptools


setuptools.setup(
    name="ochs",
    packages=["ochs"],
    version="0.3-alpha",
    license="MIT",
    description="Build static blogs based on Markdown posts, YAML files and HTML templates.",
    author="Victhor Sartório",
    author_email="victhor@vsartor.com",
    url="https://github.com/vsartor/ochs",
    keywords=["blog", "static website", "cli"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Typing :: Typed",
    ],
    entry_points="""
        [console_scripts]
        ochs=ochs.cli:ochs
    """,
)
