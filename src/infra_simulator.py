import json
import subprocess
from pathlib import Path
from src.machine import Machine
from src.validation import MachineConfig
from pydantic import ValidationError
from src.logger import logger, provisioning_logger

#define paths
CONFIG_PATH = Path("configs/instances.json")
SCRIPT_PATH = Path("scripts/setup_nginx.sh")

#get input from user
def get_raw_input():
    print("Starting machine creation.")
    print("Type 'cancel' at any time to abort.\n")

    name = input("Enter machine name: ").strip()
    if name.lower() == "cancel":
        return None

    os = input("Enter OS: ").strip().lower()
    if os.lower() == "cancel":
        return None

    cpu = input("Enter CPU cores: ").strip()
    if cpu.lower() == "cancel":
        return None

    ram = input("Enter RAM (GB): ").strip()
    if ram.lower() == "cancel":
        return None

    storage = input("Enter Storage (GB): ").strip()
    if storage.lower() == "cancel":
        return None

    return {
        "name": name,
        "os": os,
        "cpu": cpu,
        "ram": ram,
        "storage": storage,
    }

def create_machine_from_input():
    logger.info("Creating machine from user input.")
    raw_data = get_raw_input()
    if raw_data is None:
        logger.info("Machine creation cancelled by user.")
        print("Bye :(")
        return None
    
    try:
        config = MachineConfig(**raw_data) #use the raw data to fill out machine detes
    except ValidationError as e:
        print("\nInput is invalid:")
        logger.error("Validation error while creating MachineConfig")
        for err in e.errors():
            msg = err in e.errors():
            logger.error(msg)
            print(f" - {msg}")
        return None
    
    machine = Machine(
        name = config.name,
        os = config.os,
        cpu = config.cpu,
        ram = config.ram,
        storage= config.storage,
        )
    
    info = machine.to_dict()
    print("Machine created:")
    print(f"  Name: {info['name']}")
    print(f"  OS: {info['os']}")
    print(f"  CPU: {info['cpu']} Cores")
    print(f"  RAM: {info['ram']} GB")
    print(f"  Storage: {info['storage']} GB")
    return machine

def load_instances():
    if not CONFIG_PATH.exists():
        return []
    
    try:
        with CONFIG_PATH.open("r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []

def save_instances(machines: list[dict]):
    with CONFIG_PATH.open("w") as f:
        json.dump(machines, f, indent=2)

def run_nginx_setup():
    provisioning_logger.info("Running Nginx setup script.")

    try:
        result = subprocess.run(
            ["bash", "scripts/setup_nginx.sh"],
            text=True,
            capture_output=True,
        )
    except Exception as e:
        provisioning_logger.error(f"Failed to run Nginx setup script: {e}")
        print("Could not run Nginx setup script. See provisioning.log for details.")
        return
    
    if result.stdout:
        provisioning_logger.info(result.stdout)
    if result.stderr:
        provisioning_logger.error(result.stderr)
    if result.returncode != 0:
        provisioning_logger.error("Nginx setup script failed.")
        print("Nginx setup script failed. Check logs for details.")
        return
    
    provisioning_logger.info("Nginx setup script completed successfully.")
    print("Nginx setup completed successfully.")


def main():
    machine = create_machine_from_input()
    if machine is None:
        return
    
    instances = load_instances()
    instances.append(machine.to_dict())
    save_instances(instances)
    print(f"Saved {len(instances)} instances to {CONFIG_PATH}")

#looks like it will work only on linux but will log errors on other OS
    run_nginx_setup() 
#add a log catcher to determine why it fails ie "its not linux"

if __name__ == "__main__":
    logger.info("App started.")
    main()
    
