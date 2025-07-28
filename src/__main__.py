#!/usr/bin/env python3

import argparse
import json
import urllib.parse
from Flint2025_scrape import *

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--url', help='URL to scrape', required=True)
	parser.add_argument('-W', '--width', help='viewport width', type=int, default=1920)
	parser.add_argument('-H', '--height', help='viewport height', type=int, default=1080)
	parser.add_argument('-t', '--timeout', help='page load timeout', type=int, default=60)
	args = parser.parse_args()

	url = urllib.parse.urlparse(args.url, scheme='https')
	if not url.netloc:
		url = url._replace(netloc = url.path, path = '')
	
	record = safe_scrape(url.geturl(), args.width, args.height, args.timeout)
	print(json.dumps(record))

if __name__ == '__main__':
	main()
