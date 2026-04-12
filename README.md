# PyTAC

Python implementation of Test Automation Controller (TAC/Alpaca) for controlling Qualcomm debug boards.
It uses config files and PSOC firmware from the original TAC (Alpaca) system.

# Installation

    virtualenv -p python3 venv
    . ./venv/bin/activate
    pip install -r requirements.txt

## USB permissions

By default, USB devices are not accessible without root. Create a udev rule for your board:

    echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="05c6", ATTR{idProduct}=="9302", MODE="0666", GROUP="plugdev"' \
      | sudo tee /etc/udev/rules.d/99-alpaca.rules
    sudo udevadm control --reload-rules && sudo udevadm trigger

Then make sure your user is in the `plugdev` group (log out and back in after):

    sudo usermod -aG plugdev $USER

# Configuration

PyTAC requires board configuration files in a `tac_configs/` directory (default: `./tac_configs`),
which can be copied from [qcom-test-automation-controller](https://github.com/qualcomm/qcom-test-automation-controller/tree/main/configurations) project.

`devicelist.json` maps board hardware IDs to their `.tcnf` config files. Example entry for a PSOC board:

    {
      "catalog": [
        {
          "platform_id": 17,
          "configPath": "tac_configs/TAC_PSOC_17.tcnf"
        }
      ]
    }

## Finding your board's serial number

The `--serial` argument takes the USB serial number, not a device path. Find it with:

    udevadm info /dev/ttyACM0 | grep ID_SERIAL_SHORT

Or using `lsusb` (replace `VID:PID` with `0403:6011` for FTDI or `05c6:9302` for PSOC):

    lsusb -v -d VID:PID | grep iSerial

# Using as a shell

    python3 shell.py --serial <ID_SERIAL_SHORT>

Optional arguments:

    --tac-config-path ./tac_configs   # path to config directory (default: ./tac_configs)
    --log-level DEBUG                 # log verbosity (default: DEBUG)

Once started, the shell prompt accepts commands generated from your board's config script. The available commands depend on the config — not all boards define every command (e.g. newer configs may omit `powerOn`/`powerOff`). Typical commands:

**Power control:**

    powerOn
    powerOff
    devicePowerOn
    devicePowerOff
    usbDevicePowerOn
    usbDevicePowerOff

**Boot modes:**

    bootToEDL
    bootToFastboot
    bootToUEFI
    reset

**GPIO pins** (use with `1` to assert, `0` to deassert):

    pkey 1      # press power key
    pkey 0      # release power key
    volup 1
    voldn 1

Type `help` in the shell to list all commands available for your specific board.

# Using as a service

    python3 rest.py --serial <ID_SERIAL_SHORT_1> [<ID_SERIAL_SHORT_2> ...]

The REST API runs on `http://localhost:5000`. Example usage with curl:

    # List connected boards
    curl http://localhost:5000/

    # List available quick methods (bootToEDL, powerOn, etc.)
    curl http://localhost:5000/<boardid>/quick

    # Power on/off
    curl -X PUT http://localhost:5000/<boardid>/quick/powerOn
    curl -X PUT http://localhost:5000/<boardid>/quick/powerOff

    # Boot to EDL
    curl -X PUT http://localhost:5000/<boardid>/quick/bootToEDL

    # Boot to fastboot
    curl -X PUT http://localhost:5000/<boardid>/quick/bootToFastboot

    # Set a named pin
    curl -X PUT "http://localhost:5000/<boardid>/command/reset?value=1"

    # Set a raw pin (e.g., bus A, pin 0)
    curl -X PUT "http://localhost:5000/<boardid>/pin/A0?value=1"

Note: REST API server runs in debug mode. Running with multiple concurrent threads may lead to unexpected behaviour.
