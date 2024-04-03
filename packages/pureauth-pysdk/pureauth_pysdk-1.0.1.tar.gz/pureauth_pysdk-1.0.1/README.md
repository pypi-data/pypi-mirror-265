
# PureAUTH PySDK
This SDK contains functionality to sync user data to the PureAUTH server as well as the OfflineAUTH functionality.

# Development setup
For development, follow the steps below.
1) Install poetry
2) Clone the repository
3) Run command: `poetry install`
4) Run command `poetry shell`
5) Build a development wheel by running `pip install --editable .` 
6) Import the project and use. `from pureauth_pysdk import Pureauth`

A Jupyter notebook for development is provided in the docs directory. To use it, first point the notebook to the correct poetry environment for the Jupyter kernel. 
Note: After any change in the project, you need to restart the Jupyter kernel to see the changes.


# Test PyPi configuration
For publishing to Test-PyPi follow the steps below:
1) Run `poetry config repositories.test-pypi https://test.pypi.org/legacy/` to configure test-pypi
2) Run `poetry config pypi-token.test-pypi <token>` to configure the pypi token
3) Run `poetry publish --build -r test-pypi`

# Use Test-PyPi package
To use the Test-PyPi package using poetry, run the following command:
1) `poetry config repositories.test-pypi https://test.pypi.org/simple/`
2) Add these lines to the pyproject.toml file:

`[[tool.poetry.source]]` \
`name = "test-pypi"`  \
`url = "https://test.pypi.org/simple/"` \
`priority = "explicit"`

3) Under dependancies add `pureauth-pysdk = {version = "1.0.0", source = "test-pypi"}`

