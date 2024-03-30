"""
setup file for nepali package

- Building a package

    pip install build
    python -m build


- Publishing a package
You must have twine installed in your system. `pip install twine`

    python setup.py sdist bdist_wheel
    twine upload dist/*

"""
import setuptools

GITHUB_URL = "https://github.com/opensource-nepal/ad2bs"

setuptools.setup(
    name="ad2bs",
    version="0.0.0",
    license="GPL-3.0",
    author="opensource-nepal",
    author_email="aj3sshh@gmail.com, sugatbajracharya49@gmail.com",
    description="ad2bs",
    long_description="",
    long_description_content_type="text/markdown",
    keywords=[
        "nepali date conversion",
        "convert date",
        "nepali date time",
        "python convert date",
        "parse nepali date time",
        "ad2bs",
        "bs2ad"
    ],
    url=GITHUB_URL,
    packages=setuptools.find_packages(exclude=["tests*"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source": GITHUB_URL,
    },
)