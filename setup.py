#!/usr/bin/env python3
"""Setup script for mcp-todoist package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-todoist",
    version="0.1.0",
    author="",
    author_email="",
    description="Model Context Protocol (MCP) server for Todoist integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/mcp-todoist",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "todoist-api-python",
        "mcp-server>=0.5.0",
        "pydantic",
        "python-dotenv",
        "aiohttp",
    ],
    entry_points={
        "console_scripts": [
            "mcp-todoist=main:main",
        ],
    },
) 