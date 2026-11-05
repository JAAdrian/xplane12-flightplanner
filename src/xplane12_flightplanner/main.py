"""CLI tool to create a naive flightplan and export as PDF and FMS v11 file."""

import typer
from rich import print

from . import routefinder

app = typer.Typer(no_args_is_help=True)


@app.command()
def create(
    departure: str,
    arrival: str,
    min_level: int = 300,
    max_level: int = 400,
    airac_cycle: str = "2406",
):
    """Create flightplan files for desired departure and arrival in the download dir.

    Args:
        departure: the departure airport's ICAO code (e.g. EDDW)
        arrival: the arrival airport's ICAO code (e.g. EDDM)
    """
    hmtl = routefinder.get_route_from_rfinder(
        departure=departure,
        arrival=arrival,
        airac_cycle=airac_cycle,
        min_level=min_level,
        max_level=max_level,
    )
    parameter_list = routefinder.parse_rfinder_plan(html=hmtl)

    print(parameter_list[0])


def main():
    app()

if __name__ == "__main__":
    main()
