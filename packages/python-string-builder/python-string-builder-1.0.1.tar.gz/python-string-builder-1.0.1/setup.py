"""
https://github.com/wimble3
python-string-builder library.
"""
from setuptools import find_packages, setup


setup(
    name="python-string-builder",
    version="1.0.1",
    author="wimble3",
    author_email="wimble@internet.ru",
    description="StringBuilder can improve performance when connecting "
                "a large number of strings in a loop.\n"
                "It also contains additional operations on stringsю",
    long_description="See repository for more information: "
                     "https://github.com/wimble3/python-string-builder",
    long_description_content_type="text/markdown",
    url="https://github.com/wimble3",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords="string builder stringbuilder string-builder",
    project_urls={
        "GitHub": "https://github.com/wimble3"
    },
    python_requires=">=3.8"
)
