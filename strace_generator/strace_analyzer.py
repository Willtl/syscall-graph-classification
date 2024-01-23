import time

import psutil


def get_pids_by_name(app_names):
    """
    Get PIDs for processes with names in app_names.
    """
    pids = {}
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in app_names:
            pids[proc.info['pid']] = proc.info['name']
    return pids


def monitor_applications(app_names):
    """
    Monitor specified applications and log new PIDs.
    """
    known_pids = set()
    while True:
        current_pids = get_pids_by_name(app_names)
        new_pids = set(current_pids.keys()) - known_pids

        if new_pids:
            for pid in new_pids:
                print(f"New PID for {current_pids[pid]}: {pid}")
            known_pids.update(new_pids)

        time.sleep(5)  # Wait for 5 seconds before checking again


if __name__ == "__main__":
    app_names = ['chrome', 'spotify']  # List of applications to monitor
    monitor_applications(app_names)
