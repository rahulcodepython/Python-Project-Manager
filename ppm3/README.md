# ppm Package

`ppm` is a Python Project Manager CLI tool that simplifies project setup, dependency management, environment configuration, and running project commands. This tool is ideal for developers looking for a structured and efficient way to manage project dependencies, execute scripts, and configure environment variables directly from the command line. This is all in one cli tools for long pip commands.

## Overview

The `ppm` tool provides a convenient set of commands for Python project management, enabling you to:

-   **Initialize Projects**: Set up a new project structure with a default or custom configuration.
-   **Install and Uninstall Packages**: Add or remove Python packages as needed for your project.
-   **Manage Environment Variables**: Easily configure environment variables for your project.
-   **Run Project Scripts**: Execute project-specific scripts or commands from a customizable list.

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

### Commands

#### 1. `help`

Displays the help message for `ppm` and its subcommands.

**Usage:**

```bash
ppm help
```

#### 2. `version`

Displays the version of the `ppm` CLI.

**Usage:**

```bash
ppm version
```

#### 3. `init`

Initializes a new project configuration with an optional default setting.

**Usage:**

```bash
ppm init
```

**Options:**

-   `-d`: Enable default configuration.

**Example:**

```bash
ppm init -d
```

This command initializes the project using default configuration settings.

**On installation, you'll see the following prompts:**

If you have not given the flag -d then you have to answer:

```bash
project name (system)
version (1.0.0)
description ()
entry point (main.py)
author ()
license (ISC)
```

You can initiate git at the begining of the project. You will be asked

```bash
[?] Do you want to add github configuration:
 > Yes
   No

github repository name () https://github.com/rahulcodepython/New_Repo.git
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

#### 4. `install`

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

If you want to install a package from a specific version, you can use the `==` operator:

```bash
ppm install requests==2.28.2
```

This command installs the `requests` package with version 2.28.2.

If you want to install all the packages listed in `ppm.yml` file in your currect project, You can use :

```bash
ppm install
```

#### 5. `uninstall`

Uninstalls specified packages from the project.

**Usage:**

```bash
ppm uninstall <package1> <package2> ...
```

#### 6. `run`

Runs the project’s default or specified command.

**Usage:**

```bash
ppm run [command_name]
```

-   If you specify a command name (e.g., `ppm run hello`), it will execute the corresponding command defined in the configuration file.
-   If no command name is provided (i.e., `ppm run`), the default command will run.

**Examples:**

1. **Setting Up Custom Commands**:

    Suppose you define a command in your configuration file:

    ```text
     commands:
         ...
         hello: "echo 'Hello, World!'"
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

#### 7. `list`

List all packages in terminal.

**Usage:**

```bash
ppm list
```

#### 8. `freeze`

Generate `requirements.txt` file for your project packages.

**Usage:**

```bash
ppm freeze
```

#### 9. `outdated`

List all outdated packages in terminal.

**Usage:**

```bash
ppm outdated
```

#### 10. `update`

Update specified packages from the project.

**Usage:**

```bash
ppm update <package1> <package2> ...
```
