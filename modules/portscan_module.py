import nmap
import os

def perform_scan(target, log_file):
    """
    Perform an Nmap scan on the target and log the results to a file.
    """
    scanner = nmap.PortScanner()
    print(f"Scanning target: {target}")
    
    try:
        # Scan ports 1-65535 for a more comprehensive result
        scanner.scan(target, '900-999', arguments='-sV')  # -sV gives service/version info
        
        results = []
        for host in scanner.all_hosts():
            results.append(f"Host: {host} ({scanner[host].hostname()})\n")
            results.append(f"State: {scanner[host].state()}\n")
            
            for proto in scanner[host].all_protocols():
                results.append(f"Protocol: {proto}\n")
                ports = scanner[host][proto]
                for port in sorted(ports.keys()):
                    service = ports[port].get('name', 'unknown')
                    version = ports[port].get('product', '') + " " + ports[port].get('version', '')
                    state = ports[port]['state']
                    results.append(f"Port: {port}/tcp\tState: {state}\tService: {service} {version}\n")

        # Log results to file
        with open(log_file, 'w') as log:
            log.write("Nmap Scan Results:\n")
            log.writelines(results)

        print("Scan complete. Results saved to", log_file)

    except Exception as e:
        print(f"Error during scan: {e}")

def run():
    """
    Entry point for the portscan module.
    """
    target = '127.0.0.1'
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Navigate up to trojan directory
    log_file = os.path.join(base_path, 'data', 'portscan_log.txt')  # Corrected path

    # Ensure the data directory exists
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    perform_scan(target, log_file)
