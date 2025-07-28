#!/usr/bin/env python3

import base64
import datetime
import io
import json
import os
import pandas
import scapy.all
import selenium.common
import selenium.webdriver
import sys
import time
import urllib.parse

def scrape(url, width, height, timeout):
	options = selenium.webdriver.chrome.options.Options()
	options.add_argument("--allow-running-insecure-content")
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument("--disable-extensions")
	options.add_argument('--headless=new')
	options.add_argument("--hide-scrollbars")
	options.add_argument("--ignore-certificate-errors")
	#options.add_argument('--kiosk')
	options.add_argument("--no-default-browser-check")
	options.add_argument('--no-sandbox')
	#options.add_argument(f'--ozone-override-screen-size={width},{height}')
	#options.add_argument(f'--window-size={width},{height}')
	#options.add_argument(f'--start-maximized')
	#options.add_argument('--force-device-scale-factor=1')
	
	driver = selenium.webdriver.Chrome(options=options)
	sniffer = scapy.all.AsyncSniffer()
	
	driver.set_window_size(width, height)
	while True:
		""" AFAIK there is no way to avoid this. Height is sometimes slightly off """
		current_width = driver.execute_script('return window.innerWidth;')
		current_height = driver.execute_script('return window.innerHeight;')

		delta_width = width - current_width
		delta_height = height - current_height

		if delta_height or delta_width:
			new_width = width + delta_width
			new_height = height + delta_height

			driver.set_window_size(new_width, new_height)
		else:
			break
	
	
	driver.set_page_load_timeout(timeout)
	sniffer.start()
	timestamp = datetime.datetime.now()
	driver.get(url)

	load_time = datetime.datetime.now() - timestamp
	html = driver.page_source

	screenshot = driver.get_screenshot_as_base64()
	user_agent = driver.execute_script('return navigator.userAgent;')
	browser_name = driver.capabilities.get('browserName')
	browser_version = driver.capabilities.get('browserVersion')
	platform = driver.capabilities.get('platformName')
	final_url = driver.current_url
	driver.quit()
	
	packets = sniffer.stop()
	pcap_file = io.BytesIO()
	pcap_file.close = lambda:None
	scapy.all.wrpcap(pcap_file, packets)
	pcap_bytes = pcap_file.getvalue()
	pcap = base64.b64encode(pcap_bytes).decode('utf-8')
	domain = urllib.parse.urlparse(url).netloc

	record = dict()
	record['screenshot'] = screenshot
	record['html'] = html
	record['pcap'] = pcap
	record['timestamp'] = str(timestamp)
	record['user-agent'] = user_agent
	record['load-time'] = load_time.seconds
	record['browser-name'] = browser_name
	record['browser-version'] = browser_version
	record['platform'] = platform
	record['screen-height'] = current_height
	record['screen-width'] = current_width
	record['url'] = url
	record['final-url'] = final_url
	record['domain'] = domain
	record['success'] = True

	return record

def safe_scrape(*args, **kwargs):
	try:
		record = scrape(*args, **kwargs)
	except Exception as e:
		record = {'success': False, 'message': str(e)}
	return record
