# Flyover

Flyover uses [pyppeteer](https://github.com/pyppeteer/pyppeteer) to bypass Hurricane Electric's strict scraping prevention mechanisms in order to automatically gather a list of an organization's Autonomous System Numbers (ASNs).

## Installation

Clone the repository:

`git clone https://github.com/Perdyx/flyover.git`

Then, to install the necessary dependencies, run

```
cd flyover
pip install -r requirements.txt
```

*Note: It is recommended to do this inside a virtual environment to help keep your system clean. See [https://docs.python.org/3/tutorial/venv.html](https://docs.python.org/3/tutorial/venv.html) for more information.*

## Usage

`python3 flyover.py "Example Organization"`

### Scripting

To use Flyover in a script or together with other tools, you can use the `-s` option to only output a list of ASNs to STDOUT:

`python3 flyover.py "Example Organization" -s`

### Proxying requests

Hurricane Electric likes to limit queries, so to avoid getting banned easily, you can send all requests through a SOCKS5 proxy:

`python3 flyover.py "Example Organization" -p localhost:8089`

*Note: To use this, you must already have a SOCKS5 tunnel running. Running `ssh -N -D 8089 user@address` is an easy way to get one running.*
