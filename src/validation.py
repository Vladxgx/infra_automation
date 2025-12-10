from pydantic import BaseModel, field_validator
from typing import ClassVar

class MachineConfig(BaseModel):
    name: str
    os: str
    cpu: int
    ram: int  # in GB
    storage: int  # in GB

    ALLOWED_OS: ClassVar[set[str]] = {'linux', 'windows', 'macos'}

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        # Ensure the machine name is not empty
        if not value.strip():
            raise ValueError("Machine name must not be empty.")
        # ensure the machine name does not contain special characters
        if not value.isalnum():
            raise ValueError("Machine name must be alphanumeric.")
        return value

    @field_validator("os")
    @classmethod
    def allowed_os(cls, value: str) -> str:
        # normalize to lowercase and strip whitespace
        value = value.strip()
        # Check if the operating system is in the allowed list
        if value.lower() not in cls.ALLOWED_OS:
            raise ValueError(f"Operating system '{value}' is not supported. Allowed OS: {cls.ALLOWED_OS}")
        return value.lower()
    
    @field_validator("cpu", "ram", "storage")
    @classmethod
    def positive_ints(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Value must be a positive integer.")
        return value

if __name__ == "__main__":
    print("Valid example:")
    m = MachineConfig(name="vm1", os="windows", cpu=2, ram=4, storage=100)
    print(m)

    print("\nInvalid OS example:")
    try:
        MachineConfig(name="vm2", os="ubuntu", cpu=2, ram=4, storage=100)
    except Exception as e:
        print("Error for invalid OS:", e)

    print("\nInvalid CPU example:")
    try:
        MachineConfig(name="vm3", os="macos", cpu=0, ram=4, storage=100)
    except Exception as e:
        print("Error for invalid CPU:", e)

    print ("\ninvalid name example:")
    try:
        MachineConfig(name="vm@4", os="linux", cpu=2, ram=4, storage=100)
    except Exception as e:
        print("Error for invalid name:", e)