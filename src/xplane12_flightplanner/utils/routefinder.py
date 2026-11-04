"""Interface to rfinder.asalink.net."""

import requests


def get_route(
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
