import json
from pathlib import Path
from src.machine import Machine
from src.validation import MachineConfig
from pydantic import ValidationError
from src.logger import logger

CONFIG_PATH = Path("configs/instances.json")

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
        config = MachineConfig(**raw_data)
    except ValidationError as e:
        print("\nInput is invalid:")
        logger.error("Validation error while creating MachineConfig")
        for err in e.errors():
            msg = err.get("msg", "Unknown validation error")
            logger.error(f"  {msg}")
            print(f" - {msg}")
        return None
    
    machine = Machine(
        name = config.name,
        os = config.os,
        cpu = config.cpu,
        ram = config.ram,
        # storage=config.storage - add later
        )
    
    info = machine.to_dict()
    print("Machine created:")
    print(f"  Name: {info['name']}")
    print(f"  OS: {info['os']}")
    print(f"  CPU: {info['cpu']} Cores")
    print(f"  RAM: {info['ram']} GB")
    return machine

def load_instances():
    if not CONFIG_PATH.exists():
        return []
    
    try:
        with CONFIG_PATH.open("r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from the config file.")
        return []
    if not isinstance(data, list):
        print("Error: Config file format is invalid.")
        return []
    
    return data

def save_instances(machines: list[dict]):
    with CONFIG_PATH.open("w") as f:
        json.dump(machines, f, indent=2)
    
def main():
    machine = create_machine_from_input()
    if machine is None:
        return
    
    instances = load_instances()
    instances.append(machine.to_dict())
    save_instances(instances)
    print(f"Saved {len(instances)} instances to {CONFIG_PATH}")

if __name__ == "__main__":
    logger.info("App started.")
    main()
    