import os
import psutil

def run():
    """Collect system information."""
    system_info = {
        "user": os.getlogin(),
        "processes": [p.name() for p in psutil.process_iter()],
        "os": os.uname().sysname
    }
    return system_info
