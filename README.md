# infra_automation

A small Python project for creating simple “machine” configurations and running a provisioning script.  
This is part of the Rolling Project in the DevOps course.

The app lets you:

- enter machine details (name, OS, CPU, RAM, storage)
- validate them with Pydantic
- save them into `configs/instances.json`
- run a Bash script that installs nginx (or fails and logs it)

Everything is logged into the `logs/` folder.

------------------------------------

## How to run

Clone the repo:

git clone <your-repo-url>
cd infra_automation

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install requirements:

pip install -r requirements.txt

Run the simulator:

python -m src.infra_simulator

------------------------------------

## What happens when you run it

1. You get a short input flow:
   - machine name  
   - OS  
   - CPU cores  
   - RAM  
   - storage 

2. The input is validated.  
   If anything is invalid, the app tells you.

3. Valid machines are saved into:

configs/instances.json

4. After saving, the program tries to run:

scripts/setup_nginx.sh

- On Linux: installs nginx  
- On other OSes: it will fail, which is fine (the error is logged)

------------------------------------

## Logs

Two log files:

- logs/app.log – general app events  
- logs/provisioning.log – output from the nginx setup script  

If nginx fails, check provisioning.log.

------------------------------------

## Project structure

src/
    infra_simulator.py
    machine.py
    validation.py
    logger.py

scripts/
    setup_nginx.sh

configs/
    instances.json

logs/
    app.log
    provisioning.log

------------------------------------

## Notes

- The provisioning script uses apt, so it only works on Linux.
- Running it on macOS or Windows will fail, which is expected.
