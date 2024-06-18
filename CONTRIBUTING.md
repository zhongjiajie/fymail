# CONTRIBUTING

fymail use [hatch](https://hatch.pypa.io/latest/) to manage the project. Please
[install](https://hatch.pypa.io/latest/install) it before you go ahead. Run command below to install it if you
use `pip` to manage your python packages, or click [here](https://hatch.pypa.io/latest/install) for others

```shell
pip install hatch
```

## Development

### Setup Environment

```shell
# create hatch env and install dependence
hatch env create
```

## Test

create test environment only once,

```shell
hatch env create fymail-test
```

and run test in the environment

```shell
hatch test
```

## Release

* Update version: `hatch version <major|minor|micro|release>`, see [hatch version](https://hatch.pypa.io/latest/version/)
  for more detail
* Commit the version change, add new tag and push to remote, and CI will build and publish the package to PyPI

```shell
git commit -am "Release version <YOUR_VERSION_HERE>"
git tag <YOUR_VERSION_HERE>
git push origin tag <YOUR_VERSION_HERE>
```
