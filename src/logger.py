import logging
from pathlib import Path

# Make sure logs/ folder exists
Path("logs").mkdir(exist_ok=True)

# main app logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

app_handler = logging.FileHandler("logs/app.log")
app_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
app_handler.setFormatter(app_format)

logger.addHandler(app_handler)

# provisioning logger
provisioning_logger = logging.getLogger("provisioning")
provisioning_logger.setLevel(logging.INFO)

prov_handler = logging.FileHandler("logs/provisioning.log")
prov_handler.setFormatter(app_format)  # reuse same format

provisioning_logger.addHandler(prov_handler)