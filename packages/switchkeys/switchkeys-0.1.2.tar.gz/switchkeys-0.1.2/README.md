# SwitchKeys Python Client

The SwitchKeys Python Client provides a convenient way to interact with the SwitchKeys API using Python applications. This README provides an overview of the SwitchKeys Python Client, its installation process, usage instructions, and additional resources.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the SwitchKeys Python Client, you can use pip, Python's package manager. Run the following command in your terminal:

```bash
pip install switchkeys
```

## Usage

To use the SwitchKeys Python Client in your Python application, you need to import the necessary modules and initialize a SwitchKeys instance with your API token. If you don't have an API token yet, you can use the authentication methods provided by the client to obtain one and save it in a `config.ini` file for future use.

### Initializing SwitchKeys Instance

```python
from switchkeys.core.base import SwitchKeys

# If you already have an API token
switch_key = SwitchKeys(api_token="YOUR_API_TOKEN_HERE")

# If you don't have an API token yet
# Use the auth.login method to obtain tokens and save them in the config.ini file
# Or use the auth.register method to create a new user and obtain tokens
# Then initialize the SwitchKeys instance with the obtained tokens
```

### Authentication Methods

#### Logging In

```python
user = switch_key.auth.login(email="your_email@example.com", password="your_password")
# Set the token on the switchkeys instance.
SWITCH_KEY_API_TOKEN = user.access_token
switch_key.api_token = SWITCH_KEY_API_TOKEN
```

#### Registering a New User

```python
user = switch_key.auth.register(
    email="new_user@example.com",
    first_name="New",
    last_name="User",
    password="password123"
)
# Set the token on the switchkeys instance.
SWITCH_KEY_API_TOKEN = user.access_token
switch_key.api_token = SWITCH_KEY_API_TOKEN
```

After obtaining the tokens, they will be automatically saved in the `config.ini` file for future use.

## Examples

The SwitchKeys Python Client comes with several examples to demonstrate its usage for various functionalities, such as authentication, managing organizations, projects, users, etc. You can find these examples in the `examples` directory of the repository.

To run the examples, navigate to the `examples` directory and execute the Python scripts. For example:

```bash
cd examples
python auth_example.py
```

## Documentation

For detailed documentation on how to use the SwitchKeys Python Client, including available methods, parameters, and usage examples, please refer to the [official documentation](https://switchkeys-python-client-docs.com).

For more detailed documentation and usage examples, please refer to the [official documentation](https://switchkeys-python-client-docs.com).

## Contributing

Contributions to the SwitchKeys Python Client are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository.

Before contributing, please review the [contribution guidelines](./docs/CONTRIBUTING.md).

## License

The SwitchKeys Python Client is licensed under the [MIT License](LICENSE).
