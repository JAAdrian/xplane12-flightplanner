"""CLI tool to create a naive flightplan and export as PDF and FMS v11 file."""

import pathlib

import rich.console
import typer

from . import fms11, fuelplanner, routefinder

console = rich.console.Console()
app = typer.Typer(no_args_is_help=True)


@app.command()
def create(
    plane: str,
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

    with console.status("Requesting Flight Plan..."):
        html = routefinder.get_route_from_rfinder(
            departure=departure,
            arrival=arrival,
            airac_cycle=airac_cycle,
            min_level=min_level,
            max_level=max_level,
        )
    route = routefinder.parse_rfinder_plan(html=html)
    console.print("[bold green]Flight Plan Obtained")

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
    console.print("[bold green]FMS file written to " + str(fms_filename))

    with console.status("Requesting Fuel Plan..."):
        fuel = fuelplanner.get_fuel_plan(
            plane=plane, departure_icao=departure, arrival_icao=arrival
        )
    fuel = fuelplanner.parse_fuel_plan(fuel)
    console.print("[bold green]Fuel Plan Obtained")


def main():
    app()


if __name__ == "__main__":
    main()
