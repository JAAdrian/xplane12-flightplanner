"""CLI tool to create a naive flightplan and export as PDF and FMS v11 file."""

import pathlib

import typer
from rich import print

from . import fms11, routefinder

_DEBUG_MODE = False

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
    departure = departure.upper()
    arrival = arrival.upper()

    html = routefinder.get_route_from_rfinder(
        departure=departure,
        arrival=arrival,
        airac_cycle=airac_cycle,
        min_level=min_level,
        max_level=max_level,
    )

    if _DEBUG_MODE:
        with open("src/xplane12_flightplanner/example.html", "wt") as file:
            file.write(html)

    route = routefinder.parse_rfinder_plan(html=html)

    fms_filename = (
        pathlib.Path.home() / "Downloads" / f"{departure}{arrival}"
    ).with_suffix(".fms")
    fms = fms11.Fms11(
        airac_cycle=airac_cycle,
        departure_icao=departure,
        arrival_icao=arrival,
        legs=route,
    )
    fms.write(filename=fms_filename)


def main():
    app()


if __name__ == "__main__":
    main()
