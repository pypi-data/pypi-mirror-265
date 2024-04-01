from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ERA_V2_Architecture",
    version="0.1.0",
    author="Xianping Wu",
    author_email="xianpingwu@hotmail.com",
    description="The ERA-V2 course network architectures",
    long_description=long_description,
    long_description_content_type="text/markdown",    
    url="https://github.com/ping-Mel/ERAV2-Architecture.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)