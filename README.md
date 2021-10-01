# Flyover

## Installation

```
git clone https://github.com/Perdyx/flyover.git
cd flyover
pip install -r requirements.txt
```

## Usage

`python3 flyover.py "Example Organization"`

### Proxying requests

Hurricane Electric likes to limit queries, so to avoid getting banned easily, you can send all requests through a SOCKS5 proxy:

`python3 flyover.py "Example Organization" --proxy localhost:8089`

*Note: To use this, you must already have a SOCKS5 tunnel running. Running `ssh -N -D 8089 user@address` is an easy way to get one running.*
