import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-dsv-sdk",
    version="0.0.1",
    author="Adam Migus",
    author_email="adam@migus.org",
    description="The Thycotic DevOps Secrets Vault Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thycotic/python-dsv-sdk",
    install_requires=["requests>=2.12.5"],
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
