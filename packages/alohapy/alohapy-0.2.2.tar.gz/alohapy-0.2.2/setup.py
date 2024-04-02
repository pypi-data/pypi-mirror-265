# This file is used for how to bundling and publishing the package ~
from setuptools import setup, find_packages

with open("README.md", "r") as f:
  description = f.read()

setup(
  name="alohapy",
  version="0.2.2",
  packages=find_packages(),
  install_requires=[],
  entry_points={ # this would create a cli command for your aloha function and directly used by terminal ~
    "console_scripts": [
      "aloha-cli = alohapy:aloha"
    ]
  },
  long_description=description,
  long_description_content_type="text/markdown"
)
