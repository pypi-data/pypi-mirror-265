# Python CLI Tool

A command-line interface (CLI) tool written in Python for executing commands defined in a `plz.yml` file.

## Features

- Execute commands defined in a `plz.yml` file
- Customizable command names and corresponding shell commands
- Utilizes the `rich` library for enhanced console output
- Built with `typer` for easy and intuitive CLI creation

## Installation

1. Install package:

```
pip install please-do
```

## Usage

1. Create a `plz.yml` file in the current working directory with the following format:

```yaml
commands:
  - name: dev
    command: uvicorn main:app --reload # Sample for fastapi project
  - name: test
    command: pytest tests/
```

2. Run the CLI tool with the desired command name:

```
please run dev
```

As an alias you can use `plz` command
```
plz run dev
```

This will execute the corresponding command defined in the `plz.yml` file.

## Configuration

The `plz.yml` file should be placed in the current working directory and follow this structure:

```yaml
commands:
  - name: command_name
    command: shell_command
```

- `command_name`: The name you want to use to invoke the command
- `shell_command`: The actual shell command to be executed

You can define multiple commands in the `plz.yml` file.

## Error Handling

- If the `plz.yml` file is not found, an error message will be displayed, and the program will exit with a non-zero status code.
- If a command is not found in the `plz.yml` file, an error message will be displayed, and the program will exit with a non-zero status code.
- If a command fails to execute due to a `FileNotFoundError`, an error message will be displayed, and the program will exit with a non-zero status code.

## Dependencies

- Python 3.6+
- `typer`
- `rich`
- `pyyaml`

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).