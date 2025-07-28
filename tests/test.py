import base64
import io
import json
import numpy
import PIL.Image
import random
import unittest
from scrape import *

MIN_DIM = 100
MAX_DIM = 1000

BLACK_WEBSITE = """
<!DOCTYPE html>
<html>
	<head>
		<style>
			body {
				margin: 0;
				background: black;
				height: 200vh;
			}
		</style>
	</head>
	<body></body>
</html>
"""

class TestScraper(unittest.TestCase):
	def test_resolution(self):
		height = random.randint(MIN_DIM, MAX_DIM)
		width = random.randint(MIN_DIM, MAX_DIM)
		bytes = BLACK_WEBSITE.encode('utf-8')
		base64_str = base64.b64encode(bytes).decode('ascii')
		data_url = f'data:text/html;base64,{base64_str}'
		record = scrape(data_url, width, height, 60)
		screenshot_encoded = record['screenshot']
		screenshot_bin = base64.b64decode(screenshot_encoded)
		#with open('test.png', 'wb') as f: f.write(screenshot_bin)
		screenshot_file = io.BytesIO(screenshot_bin)
		screenshot = PIL.Image.open(screenshot_file)

		self.assertEqual((width, height), screenshot.size)
		
		pixels = numpy.array(screenshot.convert('RGB'))
		self.assertTrue(numpy.all(pixels == 0))

unittest.main()
