import os
import json

CONFIG_FILE = "config.json"


def set_environment_variables():
    config = load_config()
    for key, value in config.items():
        os.environ[key] = value


def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def set_environment_variable(variable, value):
    config = load_config()
    config[variable] = value
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)
    print(f"Added environment variable: {variable}={value}")