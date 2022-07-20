# AliceTRD_2022
An extension of https://github.com/tdietel/alicetrd-python.git to continue the work done on the UCT Alice Transition radiation detector. The https://github.com/mkidson/ALICE_LAB_2021.git oscilloscopeRead module is used and incorporated into the src to allow minidaq to read from the oscilloscope a well as the TRD chamber.

Installation
------------

This package uses setuptools. For now, I suggest to install it in a virtual environment:
```
python3 -m venv venv
. venv/bin/activate
python -m pip install upgrade pip
python -m pip install -r requirements.txt
python -m install -e .
```

Once installed, activate the environment with `. path/to/AliceTRD_2022/venv/bin/activate`, add `venv/bin` to the path, or run the commands with the full path `path/to/AliceTRD_2022/venv/bin/trdmon`.

Usage
-----

This section is work in progress, certainly incomplete and maybe incorrect. Read with caution, and refer to the source if in doubt.

### TRD monitor

This is a basic monitor for DCS services. It is run without any arguments: `trdmon`. Modify the source code to add more services or change the layout.

### Event dump

Parse raw data files in various formats (time frames, the historical o32 format and a new format invented for the ZeroMQ DAQ (partially) contained in this repository). 
