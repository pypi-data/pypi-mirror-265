# rocat/setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rocat",
    version="0.1.0",
    description="A simple and user-friendly library for AI services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="YumetaLab",
    author_email="root@yumeta.kr",
    url="https://github.com/root39293/rocat",
    packages=find_packages(),
    install_requires=[
        "openai",
        "streamlit",
    ],
)