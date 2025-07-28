# Installation
Install the testPyPI package:
`pip install Flint2025-scrape --index-url https://test.pypi.org/simple`
Grant the necessary capabilities to tcpdump and python3
`sudo setcap cap_net_raw=eip $(readlink -f $(which python3))`
`sudo setcap cap_net_raw=eip $(readlink -f $(which tcpdump))`

# Usage
## Commandline
`usage: Flint2025-scrape [-h] -u URL [-W WIDTH] [-H HEIGHT] [-t TIMEOUT]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to scrape
  -W WIDTH, --width WIDTH
                        viewport width
  -H HEIGHT, --height HEIGHT
                        viewport height
  -t TIMEOUT, --timeout TIMEOUT
                        page load timeout`

This will print a JSON object-string to stdout
`Flint2025-scrape -u https://example.com`
## Python3 library
This will return a Python dict
`>>> from Flint2025_scrape import scrape`
`>>> scrape('https://example.com', 1024, 1024, 1)`

