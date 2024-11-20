# ppm Package

`ppm` is a Python Project Manager CLI tool that simplifies project setup, dependency management, environment configuration, and running projects from the command line. This tool is especially useful for developers who want a streamlined way to manage project dependencies, run scripts, and configure environment variables without manually editing multiple files.

## Overview

The `ppm` tool provides a set of commands to help manage Python projects efficiently. With `ppm`, you can:

- **Initialize Projects**: Set up a new project structure with default or custom configurations.
- **Install Dependencies**: Install multiple Python packages in your project with ease.
- **Uninstall Packages**: Remove packages, with options to uninstall dependencies as well.
- **Manage Environment Variables**: Add or modify environment variables directly from the command line.
- **Run Project Scripts**: Execute the project’s main script or any other configured command.

Designed to reduce repetitive setup tasks, `ppm` enables you to focus more on coding and less on project management.

## Installation

To install `ppm`, clone the repository and run:

```bash
pip install .
```

## Usage

Use the `ppm` command followed by any of the subcommands listed below to perform various actions.

```bash
ppm <command> [options]
```

---

### Important Notes

1. **Using `ppm` as a Dependency Manager**: If you choose to use `ppm` as your dependency manager, you must specify a run script (e.g., the main Python file name or any other script you wish to run) in the project’s configuration. Without this, the `run` command will throw an error as it won’t know which script to execute.

2. **Using `ppm` with an Existing Project**: If you’re applying `ppm` to an existing project, ensure you specify `ppm` as the dependency manager when running the `ppm init` command. This will set up `ppm` to manage dependencies within your project.

---

### Commands

#### 1. `init`

Initializes a new project configuration.

**Usage:**

```bash
ppm init
```

**Options:**

- `-d`: Enable default configuration.

**Example:**

```bash
ppm init -d
```

This command initializes the project with the default configuration.

#### 2. `install`

Installs specified packages in the project.

**Usage:**

```bash
ppm install <package1> <package2> ...
```

**Example:**

```bash
ppm install requests flask
```

This command installs the `requests` and `flask` packages in the project.

#### 3. `uninstall`

Uninstalls specified packages from the project.

**Usage:**

```bash
ppm uninstall <package1> <package2> ...
```

**Options:**

- `-d`: Uninstall packages along with their dependencies.

**Example:**

```bash
ppm uninstall requests -d
```

This command uninstalls the `requests` package along with any dependencies it may have.

#### 4. `run`

Runs the project using the configuration specified in the project.

**Usage:**

```bash
ppm run
```

This command runs the project. **Note:** Ensure that a run script is specified in your project configuration when using `ppm` as a dependency manager; otherwise, this command will throw an error.

#### 5. `add_env`

Adds environment variables to an `.env` file in the project.

**Usage:**

```bash
ppm add_env <KEY=VALUE> <KEY2=VALUE2> ...
```

**Example:**

```bash
ppm add_env DATABASE_URL=mysql://user:password@localhost/dbname SECRET_KEY=your_secret_key
```

This command adds the specified key-value pairs to the project's environment file.
