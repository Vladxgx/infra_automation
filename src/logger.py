import logging
from pathlib import Path

LOG_DIR = path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_PATH = Path("logs/app.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

#main logger
logger = logging.getLogger("infra_simulator")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_PATH)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

#provisioning bash/nginx logger
proviosioning_logger = logging.getLogger("provisioning")
proviosioning_logger.setLevel(logging.INFO)

if not proviosioning_logger.handlers:
    prov_handler = logging.FileHandler(PROV_LOG_PATH)
    prov_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    prov_handler.setFormatter(prov_formatter)
    proviosioning_logger.addHandler(prov_handler)