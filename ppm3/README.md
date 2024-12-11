# ppm Package

`ppm` is a Python Project Manager CLI tool that simplifies project setup, dependency management, environment configuration, and running project commands. This tool is ideal for developers looking for a structured and efficient way to manage project dependencies, execute scripts, and configure environment variables directly from the command line. This is all in one cli tools for long pip commands.

## Overview

The `ppm` tool provides a convenient set of commands for Python project management, enabling you to:

- **Initialize Projects**: Set up a new project structure with a default or custom configuration.
- **Install and Uninstall Packages**: Add or remove Python packages as needed for your project.
- **Manage Environment Variables**: Easily configure environment variables for your project.
- **Run Project Scripts**: Execute project-specific scripts or commands from a customizable list.

The `ppm` CLI is designed to streamline project management, reducing setup time and effort so that you can focus on coding.

## Installation

To install `ppm`:

```bash
pip install ppm3
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

**On installation, you'll see the following prompts:**

Asking about how will you use ppm.

```bash
[?] How do you want to use ppm?:
   as a project manager
 > as a dependency manager
```

If you have choosen ppm as a project manager and not given the flag -d then you have to answer:

```bash
project name (system)
version (1.0.0)
description ()
entry point (main.py)
git repository ()
author ()
license (ISC)
```

You can specify required packages at the time of initialize the project.

```bash
Enter the name of the packages you want to install in the project like (<package_name>==<version>) or (<package_name>).
Packages (press Enter to end): <package1> <package2> ...
```

**Example:**

```bash
Enter the name of the packages you want to install in the project like (<package_name>==<version>) or (<package_name>).
Packages (press Enter to end): requests flask
```

This is for generating .env file.

```bash
[?] Are you sure you want to add .env file?:
   Yes
 > No
```

But if you have already .env file in your project, then you will encounter

```bash
[?] .env file already exists.:
   Overwrite
 > Keep as it is

.env file is untouched.
```

PPM will create a src folder in your root directory and inside it, it will generate a `main.py` file. If you have already this folder structure, you will be asked:

```bash
[?] Do you want to override main.py file?:
 > Yes
   No
```

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

#### 6. `list`

List all packages in terminal.

**Usage:**

```bash
ppm list
```

#### 7. `freeze`

Generate `requirements.txt` file for your project packages.

**Usage:**

```bash
ppm freeze
```
