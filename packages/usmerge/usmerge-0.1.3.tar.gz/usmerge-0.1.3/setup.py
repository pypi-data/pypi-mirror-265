import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="usmerge",
    version="0.1.3",
    description="A simple package to merge one-dimension data by unsupervised method",
    author="HuiWang",
    author_email="huiw1128@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pandas","minisom","numpy","scikit-learn"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wanghui5801/usmerge",

)
