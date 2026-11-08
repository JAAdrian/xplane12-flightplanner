"""CLI tool to create a naive flightplan and export as PDF and FMS v11 file."""

import pathlib

import rich.console
import rich.prompt
import typer

from . import DEFAULT_AIRAC_CYCLE, fms11, fuelplanner, pdf, routefinder

PDF_FILE_LOCATION = r"/home/j/X-Plane 12 Flightplans/"
FMS_FILE_LOCATION = (
    r"/mnt/j/Games/SteamLibrary/steamapps/common/X-Plane 12/Output/FMS plans/"
)

console = rich.console.Console()
app = typer.Typer(no_args_is_help=True)


def _get_filenames(
    plane: str, departure: str, arrival: str
) -> tuple[pathlib.Path, pathlib.Path]:
    fms_file_location = pathlib.Path(FMS_FILE_LOCATION)
    pdf_file_location = pathlib.Path(PDF_FILE_LOCATION)

    fms_filename = fms_file_location / f"{departure}{arrival}.fms"

    # Special case: find subdirectory
    subdirectory = "B737-800X" if plane == "B737" else plane
    pdf_filename = (
        pdf_file_location / subdirectory / f"{plane.upper()}-{departure}-{arrival}.pdf"
    )

    return fms_filename, pdf_filename


def _can_proceed(fms_filename: pathlib.Path, pdf_filename: pathlib.Path) -> bool:
    if fms_filename.is_file() and pdf_filename.is_file():
        console.print(
            "[bold red]Files already exist! Delete them first via 'delete'. Aborting..."
        )
        return False

    if fms_filename.is_file() and not pdf_filename.is_file():
        console.print(
            f"[bold yellow]The FMS file [bold]{fms_filename.name}[/bold] already "
            "exists, but the matching PDF does not."
        )
        if not rich.prompt.Confirm.ask(
            "Overwrite the FMS file and create a new file pair?",
            default=False,
            console=console,
        ):
            console.print("[bold red]Aborting...")
            return False
        else:
            return True

    return True


@app.command()
def create(
    plane: str,
    departure: str,
    arrival: str,
    min_level: int = 300,
    max_level: int = 400,
    airac_cycle: str = DEFAULT_AIRAC_CYCLE,
):
    """Create flightplan files for desired departure and arrival in the download dir.

    Args:
        plane: The desired plane type. One of A319, A320, A321, A330, A340, B737
        departure: The departure airport's ICAO code (e.g. EDDW)
        arrival: The arrival airport's ICAO code (e.g. EDDM)
        min_level: Minimum flight level for the given plan
        max_level: Maximum flight level for the given plan
        airac_cycle: Your AIRAC data's release date. This is updated eventually with
                     X-Plane versions. You can find it in your plane's FMS computer or
                     e.g. in your installation directory in the file
                     "X-Plane 12/Resources/default data/earth_awy.dat"
    """
    departure = departure.upper()
    arrival = arrival.upper()

    fms_filename, pdf_filename = _get_filenames(
        plane=plane, departure=departure, arrival=arrival
    )
    if not _can_proceed(fms_filename=fms_filename, pdf_filename=pdf_filename):
        return

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

    with console.status("Requesting Fuel Plan..."):
        fuel = fuelplanner.get_fuel_plan(
            plane=plane, departure_icao=departure, arrival_icao=arrival
        )
        fuel = fuelplanner.parse_fuel_plan(fuel)
    console.print("[bold green]Fuel Plan Obtained")

    with console.status("Writing Flight Plan..."):
        fms = fms11.Fms11(
            airac_cycle=airac_cycle,
            departure_icao=departure,
            arrival_icao=arrival,
            legs=route,
        )

        fms.write(filename=fms_filename)
        pdf.write_flight_plan(
            pdf_filename,
            route=route,
            fuel=fuel,
            departure_icao=departure,
            arrival_icao=arrival,
            plane=plane,
            min_level=min_level,
            max_level=max_level,
            airac_cycle=airac_cycle,
        )
    console.print("[bold green]FMS file written to " + str(fms_filename))
    console.print("[bold green]PDF file written to " + str(pdf_filename))


@app.command()
def delete(
    plane: str,
    departure: str,
    arrival: str,
):
    """Delete a potentially existing flightplan tuple of FMS and PDF.

    Args:
        plane: The desired plane type. One of A319, A320, A321, A330, A340, B737
        departure: The departure airport's ICAO code (e.g. EDDW)
        arrival: The arrival airport's ICAO code (e.g. EDDM)
    """
    departure = departure.upper()
    arrival = arrival.upper()

    fms_filename, pdf_filename = _get_filenames(
        plane=plane, departure=departure, arrival=arrival
    )

    if not fms_filename.is_file() and not pdf_filename.is_file():
        console.print("[bold red]No Files Found. Aborting...")
        return

    if not rich.prompt.Confirm.ask(
        "[bold yellow]Do you want to delete the currently existing flight plan files?",
        default=True,
        console=console,
    ):
        console.print("[bold red]Aborting...")
        return

    if fms_filename.is_file():
        fms_filename.unlink()
    if pdf_filename.is_file():
        pdf_filename.unlink()

    console.print("[bold green]File(s) Deleted")


def main():
    app()


if __name__ == "__main__":
    main()
