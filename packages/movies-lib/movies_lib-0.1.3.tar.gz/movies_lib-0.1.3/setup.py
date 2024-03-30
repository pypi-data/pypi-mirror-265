from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="movies_lib",
    version="0.1.3",
    author="Kirill",
    author_email="kirillgrekhovodov@gmail.com.com",
    description="Либа для лабораторной работы",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=['movie', 'movies', 'tools', 'rating'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)