import requests

def run():
    target = "http://example.com"
    for _ in range(100):
        try:
            requests.get(target)
        except requests.exceptions.RequestException:
            pass
