#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="wtu-mlflow",
    version="0.0.2",
    author="hbjs",
    author_email="hbjs97@naver.com",
    description="W-Train Utils for MLflow",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        # "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    # python_requires=">=3.8",
    python_requires=">=3.7",
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=[
        "mlflow>=1.30.1,<3.0",
        "numpy>=1.21.6",
        "boto3>=1.24.0",
        "pika>=0.13.0",
        "onnx",
        "onnxruntime",
    ],
)
