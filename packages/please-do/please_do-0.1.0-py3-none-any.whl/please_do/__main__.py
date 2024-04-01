import os
from .main import app, plz_yml_path, console

if os.path.exists(plz_yml_path):
    app(prog_name='please-do')
else:
    console.print("plz.yml not found", style="bold red")
