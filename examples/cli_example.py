import argparse
import click
from typer import Typer

def argparse_example():
    p = argparse.ArgumentParser()
    p.add_argument("--count", type=int, default=1)
    args = p.parse_args()
    print("argparse count=", args.count)

@click.command()
@click.option("--name", prompt="Your name")
def click_example(name):
    print("click name=", name)

def typer_example():
    app = Typer()

    @app.command()
    def hello(name: str):
        print(f"typer hello {name}")

    app()

if __name__ == "__main__":
    argparse_example()
    # to test click: rename entrypoint or call click_example()
    # to test typer: rename entrypoint or call typer_example()
