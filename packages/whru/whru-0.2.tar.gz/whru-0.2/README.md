# PUSH

```bash

python setup.py sdist bdist_wheel

pip install twine

# generate token on pypi

twine upload dist/*

# test whether uploading is success

pip install whru

```
