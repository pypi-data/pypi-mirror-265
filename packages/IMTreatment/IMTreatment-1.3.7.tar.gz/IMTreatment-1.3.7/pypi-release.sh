#!/bin/bash

python3 -m pip install --upgrade setuptools wheel twine bumpversion
bumpversion minor
rm -rf dist
python3 setup.py sdist bdist_wheel
twine upload dist/*
git push
git push --tags
