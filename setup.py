import setuptools
import pathlib

long_description: str = pathlib.Path('README.md').read_text(encoding='utf-8')

setuptools.setup(
    name="syenv",
    version="1.2.0",
    author="Arthuchaut",
    author_email="arthuchaut@gmail.com",
    description="A simple environment variables importer which some cool functionnalities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arthuchaut/syenv",
    packages=['syenv'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)