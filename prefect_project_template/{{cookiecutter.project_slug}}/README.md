# {{cookiecutter.project_name}}

## Getting Started

To install all dependencies and set up the project, run:

```
make install
```

This project leverages Poetry for dependency management, virtual environment handling, and packaging. This command installs Poetry (if necessary), cleans any old environments, creates a new virtual environment, installs dependencies, and sets up pre-commit hooks.

## Makefile Commands

### Prefect
This project provides Makefile commands for managing Prefect flows.

- `run`: Executes a Prefect flow run locally using your local codebase. This command allows you to test the flow on your machine while still logging to Prefect.
- `trigger`: Initiates a remote flow run on Prefect for a specified environment. Under the hood it's just `prefect deployment run '$deployment_name'`.
  - `trigger dev` (default)
  - `trigger prod`
- `deploy`: Updates the Prefect deployment for a specified environment by running the deployment script. If no environment is specified, the `APP_ENVIRONMENT` variable is checked or defaults to `dev`.
  - `deploy dev` (default)
  - `deploy prod`

### Setup and Installation
These commands handle setting up the environment, installing dependencies, and configuring essential tools.

- `default`: Runs the default setup tasks, which include `build`, `install-minimal`, and `format`. Use this command for a quick initial setup, ensuring the project is built, essential dependencies are installed, and code formatting is checked.
- `install`: Sets up the entire project environment, including installing Poetry (if needed), cleaning up old environments, creating a new virtual environment, installing all dependencies, building the project, and setting up pre-commit hooks. This is the recommended command for setting up the project fully, especially for development.
- `install-poetry`: Installs Poetry within a dedicated virtual environment if it is not already present. This command is useful for ensuring that Poetry is available to manage dependencies, and is typically run as part of the `install` process.
- `install-root`:  Installs only the root package (the main project) without any additional dependencies, even the ones listed under `[tool.poetry.dependencies]`. This is useful when you only want to install your own project code without any external libraries, typically for packaging or testing purposes.
- `install-minimal`: Installs only the core dependencies required to run the project, excluding any development or extra dependencies. This command is suitable for setting up a lean, production-like environment.
- `install-deps`: Installs all dependencies specified in `pyproject.toml`, including both core and development dependencies, along with extras. Use this command if you need the full development environment set up without performing a full project installation.
- `reinstall`: Re-installs the project environment by cleaning up any existing virtual environment, removing Poetry, and then performing a complete installation with `install`. Use this command when you want to start fresh and reset the entire environment.

### Virtual Environment Management
Commands to create, delete, or reset the virtual environment, helping maintain a clean, isolated environment.

- `new-venv`: Creates a new Python virtual environment in the specified path, typically `.venv`. This command is useful if you need to manually reset the virtual environment without running a full reinstall.
- `delete-venv`: Deletes the existing virtual environment directory, if present. Use this command to clean up the environment before setting it up fresh or if you need to remove all dependencies and environment files.
- `remove-poetry`: Removes Poetry from the dedicated virtual environment, effectively uninstalling it. This command is useful when you want to reinstall Poetry or reset its environment.

### Dependency Management
Commands focused on dependency version control and locking to ensure consistency across builds.

- `lock`: Locks dependencies without updating them, preserving the exact versions specified in the lock file. Run this command to ensure consistent builds and deployments by freezing dependencies to known versions.
- `lock-update`: Updates all dependencies and regenerates the lock file, ensuring that the latest compatible versions are specified. Use this command when you want to bring dependencies up to date for the project.

### Code Quality and Pre-commit Hooks
Commands to enforce and maintain code quality standards, including setup and updates for pre-commit hooks.

- `lint`: Checks the codebase for style and formatting compliance using `ruff`. This command is essential for ensuring that code adheres to project style guidelines, and it’s recommended to run this before committing code.
- `format`: Formats the codebase using `ruff`, applying necessary fixes to align with style standards. Use this command to automatically correct formatting issues in the code.
- `autofix-unsafe`: Runs `ruff` with additional, potentially unsafe, fixes enabled. This command can be used cautiously to automatically fix issues that may affect code behavior, so it’s recommended to review changes afterward.
- `install-hooks`: Installs pre-commit hooks to enforce code quality standards across the project. Run this after setting up dependencies to ensure that code quality checks are automatically applied during development.
- `update-hooks`: Updates pre-commit hooks to their latest versions as specified in the configuration. Use this command periodically to keep the code quality checks current.

### Testing
Commands to run the project’s test suite, ensuring functionality and reliability.

- `test`: Runs the project’s test suite using `pytest`, with verbose output. Use this command regularly to verify that all tests pass and the project behaves as expected.

### Utilities
Miscellaneous commands for general project maintenance and cleanup.

- `build`: Builds a distributable package (both source distribution and wheel) for the project. This command is useful when preparing the project for deployment or distribution, ensuring that all necessary files are bundled into an installable package.
- `clean`: Cleans up temporary files, caches, and other unwanted artifacts, including `__pycache__` folders, pytest and ruff caches, and compiled files. Run this command regularly to keep the project environment tidy.
