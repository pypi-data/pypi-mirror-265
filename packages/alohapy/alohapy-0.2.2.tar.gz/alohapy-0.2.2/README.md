# Aloha Python Package

### How to test my package locally?

```bash
# Step 1: install the testable whl file first
pip install dist/alohapy-0.2.1-py3-none-any.whl
# Step 2: run test.py file for testing my package
python test.py
# Step 2.1: Or run this cli to run the function directly:
aloha-cli
```

### Just for some recall purpose

```bash
python setup.py sdist bdist_wheel # build package locally

# also publish by twine
twine upload dist/*
# Before run that command, please create a .pypirc file and put your username and password into that file for twine to do upload credential verification process
touch .pypirc
# and put the credentials in:
[pypi]
  username = __token__
  password = YOUR_PASSWORD
```

### Anyway: first python package created 🚀🚀 ~

Happy ~
