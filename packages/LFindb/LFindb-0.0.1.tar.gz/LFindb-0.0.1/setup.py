from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="LFindb",
    version="0.0.1",
    author="Grant Ahead",
    author_email="ahead_go@qq.com",
    description=description,
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'pandas>=2.0.3',
        'mysql-connector-python>=8.3.0'
    ],
    python_requires=">=3.10",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)