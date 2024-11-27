from setuptools import find_packages, setup

setup(
    name="inia",
    version="1.0.0",
    description="Inia extends boto3 by adding missing functions and providing convenient wrappers for existing boto3 operations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="GRNET DevOps Team",
    author_email="devops-rnd@grnet.gr",
    url="https://github.com/grnet/inia",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
)
