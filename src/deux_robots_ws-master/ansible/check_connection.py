import os
import subprocess
import time
from threading import Thread
import yaml

def get_machines_from_yaml(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        machines = {}
        for group in config.values():
            for _, details in group['hosts'].items():
                ip_address = details['ansible_host']
                machines[ip_address] = False
    
    return machines

machines = get_machines_from_yaml("hosts")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def ping_loop(machine):
    while True:
        try:
            subprocess.check_output(["ping", "-c", "1", machine], stderr=subprocess.DEVNULL)
            machines[machine] = True
        except subprocess.CalledProcessError:
            machines[machine] = False
        time.sleep(1)

for machine in machines:
    machines[machine] = False
    thread = Thread(target=ping_loop, args=(machine, ), daemon=True)
    thread.start()

while True:
    clear_terminal()
    for machine in machines:
        if machines[machine]:
            print(f"\033[92m{machine} - connecté")
        else:
            print(f"\033[91m{machine} - déconnecté")
        print("\033[0m")
    time.sleep(0.2)