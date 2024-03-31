# Docs2Us PDF CLI

Docs2Us PDF CLI tool is a tool for obtaining brief stats concerning a PDF file.

## Table of Contents

- [Docs2Us PDF CLI](#docs2us-pdf-cli)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Install](#install)
    - [Runn](#runn)
  - [Developing](#developing)
    - [Prerequisites](#prerequisites)
    - [Setting up the Development Environment](#setting-up-the-development-environment)
  - [Deploying](#deploying)
  - [Contributing](#contributing)

## Getting Started

These instructions will guide you on how to install and use the Docs2Us PDF CLI tool.

### Install

Install with pip

```bash
pip install docs2us-pdf-cli
```

### Runn

The command is `pdf-stats`:

```bash
pdf-stats ~/path/to/your.pdf
{
    "can_open": true,
    "has_toc": false,
    "is_pdf": true,
    "password_protected": false,
    "pdf_version": "1.3",
    "size_bytes": 827244,
    "size_pages": 12
}
```

## Developing

### Prerequisites

- Python 3.10 or higher
- Poetry (Python dependency management tool)

If you haven't installed Poetry yet, you can find the installation instructions [here](https://python-poetry.org/docs/#installation).

### Setting up the Development Environment

1. Clone the Docs2Us PDF CLI repository to your local machine.
2. Navigate to the root directory of the cloned repository.
3. Run the following command to install the necessary dependencies:

    ```bash
    poetry install
    ```

4. To build the package with any changes, increase the version in `pyproject.toml` and build:

    ```bash
    poetry build
    poetry install
    ```

## Deploying

Test PyPi:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi YOUR_TEST_PYPI_TOKEN
poetry publish --repository testpypi
pip install --index-url https://test.pypi.org/simple/ YOUR_PACKAGE_NAME
```

## Contributing

We welcome contributions from everyone. Here are a few guidelines to help you get started:

1. **Fork the Repository**: Start by forking the Docs2Us PDF CLI repository to your own GitHub account.
2. **Clone the Repository**: Clone the forked repository to your local machine.
3. **Create a New Branch**: Always create a new branch for your changes. This keeps the commit history clean and easy to navigate.
4. **Make Your Changes**: Make your changes in the new branch. Be sure to test your changes!
5. **Commit Your Changes**: Commit your changes regularly with clear, concise commit messages.
6. **Push Your Changes**: Once you're happy with your changes, push them to your forked repository.
7. **Submit a Pull Request**: Finally, submit a pull request from your forked repository to the original Docs2Us PDF CLI repository. Be sure to provide a clear description of the changes you've made.

Before contributing, please read our [Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

Thank you for your interest in contributing to Docs2Us!
