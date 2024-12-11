import os
import time
import json
import random
import importlib
from github_helper import fetch_config, upload_results

CONFIG_PATH = "config/config.json"
DATA_PATH = "data/results/"

def load_config():
    """Load configuration from the local JSON file."""
    with open(CONFIG_PATH, 'r') as file:
        return json.load(file)

def run_module(module_name):
    """Dynamically load and execute a module."""
    try:
        module = importlib.import_module(f"modules.{module_name}")
        result = module.run()
        save_results(module_name, result)
    except Exception as e:
        print(f"Error running {module_name}: {e}")

def save_results(module_name, result):
    """Save module results to the data folder."""
    result_file = os.path.join(DATA_PATH, f"{module_name}_results.json")
    with open(result_file, 'w') as file:
        json.dump(result, file)
    upload_results(result_file)  # Upload to GitHub.

def main():
    while True:
        config = fetch_config()  # Fetch the latest config from GitHub.
        if config.get("modules_to_run"):
            for module in config["modules_to_run"]:
                run_module(module)
        time.sleep(config.get("poll_interval", 300))

if __name__ == "__main__":
    main()
