from setuptools import find_packages, setup

setup(
    name="inia",
    version="1.0.0",
    description="Inia is a Python library that implements functions not included in boto3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="GRNET DevOps",
    author_email="devops-rnd@grnet.gr",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
)
