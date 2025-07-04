from setuptools import find_packages, setup

setup(
    name="inia",
    version="1.0.0-dev",
    description="Inia extends boto3 by adding missing functions and providing convenient wrappers for existing boto3 operations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="GRNET DevOps Team",
    author_email="devops-rnd@grnet.gr",
    url="https://github.com/grnet/inia",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        # The boto version ranges are added to support usage in
        # procloud! Be careful when updating these!
        "boto3 ==  1.38.5",
        "botocore == 1.38.5",
        "requests == 2.32.4",
        "requests-aws4auth == 1.3.1", ],
)
