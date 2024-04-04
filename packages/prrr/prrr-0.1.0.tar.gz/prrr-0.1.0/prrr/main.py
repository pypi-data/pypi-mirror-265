import typer

from prrr.commands.init import generate_config_file
from prrr.commands.pr import app as generate

app = typer.Typer()
app.add_typer(generate, name="pr", help="Generate a Pull Request")


@app.command()
def init():
    print("Initializing project")
    generate_config_file()


if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(f"Error: {e}")
