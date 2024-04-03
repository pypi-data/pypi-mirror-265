from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "My First Test Python package"
LONG_DESCRIPTION = "This is my first test python package. Maybe use it as a template later."

setup(
    # the name must match the package name - verysimpletest
    name="verysimpletest",
    version=VERSION,
    author="LinkunGao",
    author_email="gaolinkun123@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # Add any packages if you use it in your packages
    install_requires=[],
    keywords=['python', 'test'],
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "License :: OSI Approved :: Apache Software License"
    ]
)