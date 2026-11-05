"""Tools for handling FMS v11 files for X-Plane 12."""

DEFAULT_AIRAC_CYCLE = "2406"


class Fms11:
    """Create FMS v11 files."""

    def __init__(self):
        """Instantiate the object."""
        self.airac_cycle: str = DEFAULT_AIRAC_CYCLE
        self.departure_icao: str = ""
        self.destination_icao: str = ""
        self.waypoints: list[str] = [""]

    def create(self, filename: str = "flightplan.fms"):
        """Create the FMS file."""
        num_waypoints = len(self.waypoints)

        with open(filename, "wt") as file:
            file.write("I\n")
            file.write("1100 Version\n")
            file.write(f"CYCLE {self.airac_cycle}")
            file.write(f"ADEP {self.departure_icao}")
            file.write(f"ADES {self.destination_icao}")

            file.write(f"NUMENR {num_waypoints}")
            file.writelines(self.waypoints)
