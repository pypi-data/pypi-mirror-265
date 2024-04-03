import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codedepot-git-ai",
    version="0.0.2",
    author="CodeDepot",
    author_email="contact@codedepot.ai",
    description="Dataset and model support for git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codedepot-ch/git-ai",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/git-ai'],
    install_requires=[
        'tensorboard',
        'torch',
        'pygit2'
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
)
