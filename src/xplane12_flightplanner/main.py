"""CLI tool to create a naive flightplan and export as PDF and FMS v11 file."""

import typer
from rich import print

from . import routefinder

app = typer.Typer()


@app.command()
def print_test_route():
    departure = "EDDM"
    arrival = "EDDH"

    html = routefinder.get_route_from_rfinder(departure=departure, arrival=arrival)
    print(html)


@app.command()
def try_beautifulsoup():
    from bs4 import BeautifulSoup

    departure = "EDDM"
    arrival = "EDDH"

    html = routefinder.get_route_from_rfinder(departure=departure, arrival=arrival)
    soup = BeautifulSoup(html, "html.parser")
    print(soup)

def main():
    app()
