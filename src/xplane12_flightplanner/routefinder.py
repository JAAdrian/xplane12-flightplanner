"""Interface to rfinder.asalink.net."""

import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from . import DEFAULT_AIRAC_CYCLE

_RFINDER_URL = r"https://rfinder.asalink.net/free/autoroute_rtx.php"

_LEG = re.compile(
    r"\s*(?P<id>\w+)\s+(?P<freq>\d+\.?\d+)?\s+(?P<trk>\d+)\s+(?P<dist>\d+)\s+"
    r"(?P<lat>[NS0-9°\\'\".]+)\s+(?P<lon>[EW0-9°\\'\".]+)\s+(?P<name>\w+)"
)

_COORD = re.compile(
    r"(?P<prefix>[NSWE]{1})"
    r"(?P<degree>\d{1,3})(?:°{1})"
    r"(?P<minute>\d{1,2})(?:\')"
    r"(?P<second>\d{1,2}\.\d+)(?:\")"
)

_VIA = re.compile(r"(?<=-)([\w\d]+)(?=->)")


@dataclass
class RouteItem:
    id: str
    longitude: str | float
    latitude: str | float
    trk: int
    dist: int
    name: str
    freq: str = ""
    type: int = 11
    via: str = ""

    def __post_init__(self):
        if isinstance(self.longitude, str) and "'" in self.longitude:
            fixed_coordinate = self._fix_coordinate(self.longitude)
            self.longitude = fixed_coordinate
        if isinstance(self.latitude, str) and "'" in self.latitude:
            fixed_coordinate = self._fix_coordinate(self.latitude)
            self.latitude = fixed_coordinate

    def _fix_coordinate(self, coordinate):
        match = _COORD.search(coordinate)
        assert match is not None

        groups = match.groupdict()
        decimal_degrees = (
            float(groups["degree"])
            + float(groups["minute"]) / 60
            + float(groups["second"]) / 3600
        )
        sign = -1 if groups["prefix"] in ["S", "W"] else 1

        return sign * decimal_degrees


def route_from_dict(match_dict: dict) -> RouteItem:
    route = RouteItem(
        id=match_dict["id"],
        longitude=match_dict["lon"],
        latitude=match_dict["lat"],
        trk=int(match_dict["trk"]),
        dist=int(match_dict["dist"]),
        name=match_dict["name"],
        freq=match_dict["freq"] or "",
    )
    if route.freq:
        route.type = 3

    return route


def get_route_from_rfinder(
    departure: str = "",
    arrival: str = "",
    airac_cycle: str = DEFAULT_AIRAC_CYCLE,
    min_level: int = 300,
    max_level: int = 400,
    level: str = "B",
) -> str:
    payload = {
        "id1": departure,
        "id2": arrival,
        "minalt": f"FL{min_level}",
        "maxalt": f"FL{max_level}",
        "lvl": level,
        "dbid": airac_cycle,
        "usesid": "Y",
        "usestar": "Y",
        "easet": "Y",
        "rnav": "Y",
        "nats": "R",
    }

    response = requests.post(
        _RFINDER_URL,
        data=payload,
        timeout=60,
    )
    response.raise_for_status()

    return response.text


def parse_rfinder_plan(html: str) -> list[RouteItem]:
    soup = BeautifulSoup(html, "html.parser")

    body = soup.find("body")
    assert body is not None, "No body found in HTML"

    # find the leg table
    legs = body.find("pre")
    assert legs is not None, "No leg table found in HTML body"

    # parse the leg table
    table = legs.text.splitlines()
    departure_processed = False
    route = []
    for line in table:
        if "ID" in line:
            continue
        matches = _LEG.search(line)
        assert matches is not None, "Leg item was not parsed from leg table"

        groups = matches.groupdict()
        leg = route_from_dict(groups)

        # set type and via for the departure airport (i.e. first element)
        if not departure_processed:
            leg.type = 1
            leg.via = "ADEP"
            departure_processed = True

        route.append(leg)

    # set type and via for the arrival airport (i.e. last element)
    route[-1].type = 1
    route[-1].via = "ADES"

    # find the VIAs
    vias = _VIA.findall(body.text)
    assert vias, "No VIAs parsed from HTML body"
    assert len(vias) == (len(route) - 1), "The number of VIAs did not match the legs."

    # apply VIAs
    leg_counter = -1
    for leg in route:
        if leg.via in ["ADEP", "ADES"]:
            continue
        leg_counter += 1

        this_via = vias[leg_counter]
        if this_via == "SID":
            leg.via = "DRCT"
            continue

        leg.via = this_via

    return route
