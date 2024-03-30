# Build package

Compile:
```bash
python setup.py sdist
```

Upload package to PyPi.org
```bash
twine upload --repository testpypi dist/* --config-file .pypirc
```

