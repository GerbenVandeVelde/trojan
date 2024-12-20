import time
import json
import importlib
import random
from github_integration import GithubIntegration

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    github = GithubIntegration(config['client_id'])

    while True:
        github.pull_config()
        modules_to_run = config.get('modules', [])
        for module_name in modules_to_run:
            module = importlib.import_module(f"modules.{module_name}")
            module.run()
        
        sleep_time = random.randint(config['poll_interval'], config['poll_interval'] + 10)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
