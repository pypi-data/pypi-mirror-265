import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws_ecr_boto3",                     # This is the name of the package
    version="0.0.5",                        # The initial release version
    author="Rukmal Senavirathne",                     # Full name of the author
    description="Create and delete aws ecr repository using python boto3 like terraform ",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    # packages=setuptools.find_packages(),
    p0ackages=setuptools.find_packages(where="src"),  # Adjusted to find packages within 'src' directory
    package_dir={"": "src"}, # Directory of the source code of the packageList of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package           # Name of the python package
    # package_dir={'':'aws_ecr\src'},
    install_requires=['boto3']                     # Install other dependencies if any
)