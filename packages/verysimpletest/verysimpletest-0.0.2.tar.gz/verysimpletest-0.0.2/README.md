# test_py_pack

## Build package

```shell
python setup.py sdist bdist_wheel
```

## Upload package to PyPi

- Install twine
```shell
pip install twine
```

- Upload package

```shell
python -m twine upload dist/*
```