import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="signpdf2",
    version="7.0.0",
    description="Sign PDFs using a signature image",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aseem-hegshetye/signpdf",
    author="Aseem Hegshetye",
    author_email="aseem.hegshetye@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    packages=["signpdf2"],
    include_package_data=True,
    install_requires=["pypdf", "requests", "urllib3", "reportlab", "pytz"],

)
