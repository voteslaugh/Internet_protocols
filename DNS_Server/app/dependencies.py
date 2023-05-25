import json


def get_server_settings() -> dict:
    with open("config.json", "r") as f:
        settings = json.load(f)
    return settings
