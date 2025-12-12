class Machine:
    def __init__(self, name: str, os: str, cpu: int, ram: int, storage: int):
        self.name = name
        self.os = os
        self.cpu = cpu
        self.ram = ram
        self.storage = storage

    def to_dict(self):
        return {
            "name": self.name,
            "os": self.os,
            "cpu": self.cpu,
            "ram": self.ram,
            "storage": self.storage,
        }
