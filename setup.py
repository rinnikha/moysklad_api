"""
Setup script for the MoySklad API client.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="moysklad-api",  # Changed from "r-moysklad-api"
    version="0.1.0",
    author="Rustam Minnikhanov",
    author_email="minnikhanovrusdev@gmail.com",
    description="A comprehensive Python client for the MoySklad JSON API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rinnikha/moysklad_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
    ],
)