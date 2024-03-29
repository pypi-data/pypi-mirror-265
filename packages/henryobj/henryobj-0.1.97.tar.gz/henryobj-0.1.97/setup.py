from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="henryobj",
    version="0.1.97", # need to increment this everytime otherwise Pypi will not accept the new version
     url='https://github.com/HenryObj/mypip',
    packages=find_packages(),
    install_requires=[
        "openai>=1.9.0",
        "tiktoken>=0.5.2",
        "requests>=2.31.0",
        "bs4",
        "pathspec"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)