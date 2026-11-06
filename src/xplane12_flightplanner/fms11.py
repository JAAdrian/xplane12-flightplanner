"""Tools for handling FMS v11 files for X-Plane 12."""

import pathlib

from . import routefinder

_DEFAULT_AIRAC_CYCLE = "2406"
_REQUIRED_ALTITUDE = 0


class Fms11:
    """Create FMS v11 files."""

    def __init__(
        self,
        airac_cycle: str,
        departure_icao: str,
        arrival_icao: str,
        legs: list[routefinder.RouteItem],
    ):
        """Instantiate the object."""
        self.airac_cycle: str = airac_cycle or _DEFAULT_AIRAC_CYCLE
        self.departure_icao: str = departure_icao or ""
        self.destination_icao: str = arrival_icao or ""
        self.legs: list[routefinder.RouteItem] = legs or []

    def write(self, filename: pathlib.Path = pathlib.Path("flightplan.fms")):
        """Create the FMS file."""
        num_waypoints = len(self.legs)

        with open(filename, "wt") as file:
            file.write("I\n")
            file.write("1100 Version\n")
            file.write(f"CYCLE {self.airac_cycle}\n")
            file.write(f"ADEP {self.departure_icao}\n")
            file.write(f"ADES {self.destination_icao}\n")

            file.write(f"NUMENR {num_waypoints}\n")
            for leg in self.legs:
                leg_string = (
                    f"{leg.type} {leg.id} {leg.via} {_REQUIRED_ALTITUDE:.6f} "
                    f"{leg.latitude:.6f} {leg.longitude:.6f}\n"
                )
                file.write(leg_string)
