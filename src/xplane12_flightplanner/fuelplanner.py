"""Interface and tools to request a fuel plan from fuelplanner.com."""

import re
from dataclasses import dataclass

import bs4
import requests

_FUELPLANNER_URL = r"https://fuelplanner.com/"


@dataclass
class FuelItem:
    block_fuel: int
    reserve_fuel: int
    total_fuel: int


def _get_oew(plane: str) -> int:
    map = {
        "A319": 89900,
        "A320": 97700,
        "A321": 110500,
        "A330": 275600,
        "A340": 392400,
        "B737": 91300,
    }
    return map[plane]


def _get_ttl(plane: str) -> int:
    map = {
        "A319": 31200,
        "A320": 35300,
        "A321": 45000,
        "A330": 78400,
        "A340": 118200,
        "B737": 36200,
    }
    return map[plane]


def _sanitize_plane(plane: str) -> str:
    map = {
        "A319": "A319",
        "A320": "A320",
        "A321": "A321",
        "A330": "A332",
        "A340": "A343",
        "B737": "B738_ZIBO",
    }
    return map[plane]


def get_fuel_plan(plane: str, departure_icao: str, arrival_icao: str) -> str:
    oew = _get_oew(plane)
    ttl = _get_ttl(plane)

    sane_plane = _sanitize_plane(plane)

    payload = {
        "okstart": 1,
        "EQPT": sane_plane,
        "ORIG": departure_icao,
        "DEST": arrival_icao,
        "submit": "PLANNER",
        "RULES": "FARDOM",
        "TANKER": "",
        "UNITS": "LBS",
        "OEW": oew,
        "TTL": ttl,
    }

    response = requests.post(
        _FUELPLANNER_URL,
        data=payload,
        timeout=60,
    )
    response.raise_for_status()

    return response.text


def parse_fuel_plan(html: str) -> FuelItem:
    soup = bs4.BeautifulSoup(html, "html.parser")

    table = soup.find(lambda tag: tag.name == "table")
    assert table is not None

    rows: list[bs4.element.Tag] = table.findAll(lambda tag: tag.name == "tr")  # type: ignore
    assert rows is not None

    block_fuel = 0
    reserve_fuel = 0
    total_fuel = 0
    for row in rows:
        contents = row.contents
        assert contents is not None

        if "Fuel Usage" in contents[0]:  # type: ignore
            block_fuel = int(contents[1].text)
        elif "Reserve Fuel" in contents[0]:  # type: ignore
            reserve_fuel = int(contents[1].text)
        elif "Fuel on Board" in contents[0]:  # type: ignore
            total_fuel = int(contents[1].text)
        else:
            continue

    return FuelItem(
        block_fuel=block_fuel, reserve_fuel=reserve_fuel, total_fuel=total_fuel
    )
