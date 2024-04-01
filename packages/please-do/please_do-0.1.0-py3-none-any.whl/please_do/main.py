import sys

from rich.console import Console
from rich import print
import typer
import subprocess
import os
import yaml

app = typer.Typer()
console = Console()
cwd = os.getcwd()
plz_yml_path = os.path.join(cwd, 'plz.yml')


def parse_plz_yml():
    with open(plz_yml_path, 'r') as file:
        return yaml.safe_load(file)


@app.command()
def run(command_name: str):
    plz_yml = parse_plz_yml()
    commands = plz_yml.get('commands', [])
    command = next((cmd for cmd in commands if cmd.get('name') == command_name), None)
    if not command or not (command_str := command.get('command')):
        return console.print(f"Command `{command_name}` not found", style="bold red")
    try:
        process = subprocess.Popen(command_str.split(' '), stdout=sys.stdout, stderr=sys.stderr, text=True)
        process.wait()
    except FileNotFoundError as e:
        print(e)


@app.command()
def say(name: str):
    print(f"Here's the data {name}")
