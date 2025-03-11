# PyTAC

This is implementation of Test Automation Controller
It only uses config files and PSOC firmware from original TAC (Alpaca)

# Installation

    virtualenv -p python3 venv
    . ./venv/bin/activate
    pip install -r requirements.txt

# Using as a service

    python3 rest.py --serial <ID_SERIAL_SHORT of the debug board 1> <ID_SERIAL_SHORT of the debug board 2> ...

Note: REST API server runs in debug mode. Currently this is the only supported option
Running with multiple concurrent threads may lead to unexpected behaviour.

# Using as shell

    python3 shell.py --serial <ID_SERIAL_SHORT of the debug board>
