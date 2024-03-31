Started : 23 March 2024
Published : 30 March 2025
Finished : ????

Link : https://packaging.python.org/en/latest/tutorials/packaging-projects/

Link2 : https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#uploading-your-project-to-pypi

##### Pure Python Wheels
python3 -m build --wheel

### Upload your distributions
Once you have an account you can upload your distributions to PyPI using twine.

The process for uploading a release is the same regardless of whether or not the project already exists on PyPI - if it doesn’t exist yet, it will be automatically created when the first release is uploaded.

For the second and subsequent releases, PyPI only requires that the version number of the new release differ from any previous releases.
##### upload project to pypi
twine upload dist/*