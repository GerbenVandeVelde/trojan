import os
import platform
import subprocess

def get_system_info():
    """Retrieve basic system information."""
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture()[0],
        "Hostname": platform.node(),
        "Processor": platform.processor()
    }
    return system_info

def get_users():
    """Retrieve a list of users on the system."""
    try:
        if platform.system() == "Windows":
            users = subprocess.check_output("net user", shell=True, text=True)
        else:
            users = subprocess.check_output("cut -d: -f1 /etc/passwd", shell=True, text=True)
        return users.strip().split("\n")
    except Exception as e:
        return [f"Error retrieving users: {str(e)}"]

def get_running_processes():
    """Retrieve a list of running processes."""
    try:
        if platform.system() == "Windows":
            processes = subprocess.check_output("tasklist", shell=True, text=True)
        else:
            processes = subprocess.check_output("ps -aux", shell=True, text=True)
        return processes.strip().split("\n")
    except Exception as e:
        return [f"Error retrieving processes: {str(e)}"]

def save_results(log_file, system_info, users, processes):
    """Save the collected information to a log file."""
    with open(log_file, "w") as log:
        log.write("System Information:\n")
        for key, value in system_info.items():
            log.write(f"{key}: {value}\n")
        log.write("\nUsers:\n")
        log.writelines(f"{user}\n" for user in users)
        log.write("\nRunning Processes:\n")
        log.writelines(f"{process}\n" for process in processes)

def run():
    """Main function to run the system enumeration module."""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Navigate up to trojan directory
    log_file = os.path.join(base_path, 'data', 'system_enumeration_log.txt')

    # Ensure the data directory exists
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    print("Collecting system information...")
    system_info = get_system_info()

    print("Collecting user accounts...")
    users = get_users()

    print("Collecting running processes...")
    processes = get_running_processes()

    print("Saving results to log file...")
    save_results(log_file, system_info, users, processes)

    print(f"System enumeration complete. Results saved to {log_file}")

if __name__ == "__main__":
    run()
