# ppm Package

`ppm` is a Python Project Manager CLI tool that simplifies project setup, dependency management, environment configuration, and running project commands. This tool is ideal for developers looking for a structured and efficient way to manage project dependencies, execute scripts, and configure environment variables directly from the command line.

## Overview

The `ppm` tool provides a convenient set of commands for Python project management, enabling you to:

- **Initialize Projects**: Set up a new project structure with a default or custom configuration.
- **Install and Uninstall Packages**: Add or remove Python packages as needed for your project.
- **Manage Environment Variables**: Easily configure environment variables for your project.
- **Run Project Scripts**: Execute project-specific scripts or commands from a customizable list.

The `ppm` CLI is designed to streamline project management, reducing setup time and effort so that you can focus on coding.

## Installation

To install `ppm`, clone the repository and run:

```bash
pip install .
```

## Usage

Use the `ppm` command followed by any of the subcommands listed below to manage various aspects of your project.

```bash
ppm <command> [options]
```

### Important Notes

1. **Using `ppm` as a Dependency Manager**: If you choose to use `ppm` as your dependency manager, be sure to specify a run script (e.g., a Python filename or any other command you wish to execute) in the configuration file. Without this, the `run` command will throw an error as it will not have a script to execute.

2. **Using `ppm` on an Existing Project**: If you’re applying `ppm` to an existing project, specify `ppm` as the dependency manager when running `ppm init`. This setup will integrate `ppm` as the dependency manager for your project.

---

### Commands

#### 1. `init`

Initializes a new project configuration with an optional default setting.

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

This command initializes the project using default configuration settings.

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

This command installs the `requests` and `flask` packages in your project.

#### 3. `uninstall`

Uninstalls specified packages from the project, with an option to include dependencies.

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

This command uninstalls the `requests` package and any dependencies.

#### 4. `run`

Runs the project’s default or specified command.

**Usage:**

```bash
ppm run [command_name]
```

- If you specify a command name (e.g., `ppm run hello`), it will execute the corresponding command defined in the configuration file.
- If no command name is provided (i.e., `ppm run`), the default command will run.

**Examples:**

1. **Setting Up Custom Commands**:

   Suppose you define a command in your configuration file:

   ```text
   hello = "python hello.py"
   ```

   You can run this command with:

   ```bash
   ppm run hello
   ```

2. **Running the Default Command**:

   If you want to run the default command specified in your configuration file, simply use:

   ```bash
   ppm run
   ```

#### 5. `add_env`

Adds key-value pairs to the project’s `.env` file.

**Usage:**

```bash
ppm add_env <KEY=VALUE> <KEY2=VALUE2> ...
```

**Example:**

```bash
ppm add_env DATABASE_URL=mysql://user:password@localhost/dbname SECRET_KEY=your_secret_key
```

This command adds the specified environment variables to the `.env` file.
