from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="telegram-markdown-text",
    version="0.2",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown'
)
