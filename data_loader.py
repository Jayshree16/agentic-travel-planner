import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str):
    """
    Load JSON data from data folder.
    """
    try:
        with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"{filename} not found in data folder")
    except json.JSONDecodeError:
        raise Exception(f"{filename} is not valid JSON")


def load_flights():
    return load_json("flights.json")


def load_hotels():
    return load_json("hotels.json")


def load_places():
    return load_json("places.json")
