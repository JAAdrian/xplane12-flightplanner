"""Interface to rfinder.asalink.net."""

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class RouteEntities:
    x: int = 5


def get_route_from_rfinder(
    departure: str = "",
    arrival: str = "",
    airac_cycle: str = "2406",
    min_level: int = 300,
    max_level: int = 400,
    level: str = "B",
):
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
        "https://rfinder.asalink.net/free/autoroute_rtx.php",
        data=payload,
        timeout=60,
    )
    response.raise_for_status()

    return response.text


def parse_rfinder_plan(html: str):
    soup = BeautifulSoup(html, "html.parser")
