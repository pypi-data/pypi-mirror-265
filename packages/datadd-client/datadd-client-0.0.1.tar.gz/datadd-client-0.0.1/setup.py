import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datadd-client",
    version="0.0.1",
    author="Sam Hjelmfelt",
    author_email="sam@helm.news",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://helm.news",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)