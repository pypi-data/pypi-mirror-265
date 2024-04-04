from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="easyted",  
    version="0.0.3",
    author="Lasal Jayawardena",  
    author_email="lasalcjl@gmail.com", 
    description="A Python library for easy calculation of tree edit distances with visualization capabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LasalJayawardena/easyted", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'nltk>=3.5',
        'stanza>=1.2',
        'apted>=1.0',
    ],
)
