import typer
from rich import print

from xplane12_flightplanner.utils import routefinder

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@app.command()
def test_route():
    departure = "EDDM"
    arrival = "EDDH"

    html = routefinder.get_route(departure=departure, arrival=arrival)
    print(html)


def main():
    app()
