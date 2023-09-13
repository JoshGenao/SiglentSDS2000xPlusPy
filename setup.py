import setuptools

setuptools.setup(
    name = "SiglentSDS2000XPlusPy",
    version = "0.1",
    author = "Josh Genao",
    author_email = "jgenao622@gmail.com",
    description = "Python library to control Siglent SDS2000X Plus oscilloscope",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)