"""
Setup script for czastc package.
"""
import setuptools
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
setuptools.setup(
    name="czastc",
    version="0.0.1a6",
    author="CZAsTC",
    license="Apache-2.0",
    author_email="chensukai43@outlook.com",
    description="A testing python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CZAsTc/CZAsTc-Python-Library",
    classifiers=[
        "Development Status :: 3 - Alpha", 
        "License :: OSI Approved :: Apache Software License", 
        "Programming Language :: Python :: 3", 
        "Operating System :: OS Independent", 
    ]
)
