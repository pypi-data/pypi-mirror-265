from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fp:
  long_description = fp.read()

setup(
  name='snqueue',
  version='0.7.1',
  description='A message-driven req/res implementation using AWS SNS/SQS',
  long_description=long_description,
  long_description_content_type="text/markdown",
  package_dir={"": "src"},
  packages=find_namespace_packages(where="src"),
  install_requires=[
    "boto3",
    "pycryptodomex",
    "pydantic[email]",
    "pydantic-settings",
    "python-dateutil"
  ]
)