import json
from pathlib import Path
from src.machine import Machine
from src.validation import MachineConfig
from pydantic import ValidationError

CONFIG_PATH = Path("configs/machines.json")

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
    raw_data = get_raw_input()
    
    if raw_data is None:
        print("Bye :(")
        return None
    
    try:
        config = MachineConfig(**raw_data)
    except ValidationError as e:
        print("\nInput is invalid:")
        for err in e.errors():
            print(f" - {err['msg']}")
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

def load_machines():
    """Load existing machines from JSON and return a list."""
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

def save_machines(machines: list[dict]):
    with CONFIG_PATH.open("w") as f:
        json.dump(machines, f, indent=2)
    
def main():
    machine = create_machine_from_input()
    if machine is None:
        return
    
    machines = load_machines()
    machines.append(machine.to_dict())
    save_machines(machines)
    print(f"Saved {len(machines)} machines to {CONFIG_PATH}")

if __name__ == "__main__":
    main()