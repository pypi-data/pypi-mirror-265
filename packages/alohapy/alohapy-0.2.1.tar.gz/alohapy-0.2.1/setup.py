# This file is used for how to bundling and publishing the package ~
from setuptools import setup, find_packages

setup(
  name="alohapy",
  version="0.2.1",
  packages=find_packages(),
  install_requires=[],
  entry_points={ # this would create a cli command for your aloha function and directly used by terminal ~
    "console_scripts": [
      "aloha-cli = alohapy:aloha"
    ]
  }
)
