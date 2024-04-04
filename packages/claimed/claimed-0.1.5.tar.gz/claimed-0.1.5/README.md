# Install

```bash
pip install claimed
```

This package installs the [CLAIMED Component Compiler (C3)](https://pypi.org/project/claimed-c3/) and the [CLAIMED CLI tool](https://pypi.org/project/claimed-cli/) which can be used to run operators locally. 


# Build & Publish
```bash
python -m build # might require a 'pip install build'
python -m twine upload --repository pypi dist/* # might require a 'pip install twine'
rm -r dist
```
