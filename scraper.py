import pycurl
import re

################
# The following code was originally based on pycurl's examples/quickstart/response_headers.py

try:  # Flipped the try and except clauses to silence a persistent inspection warning
	from StringIO import StringIO as BytesIO
except ImportError:
	from io import BytesIO

def setupResp():
	r = pycurl.Curl()
	r.setopt(pycurl.USERAGENT,
			 "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
	r.setopt(pycurl.FOLLOWLOCATION, 1)
	r.setopt(pycurl.SSL_VERIFYPEER, 1)
	r.setopt(pycurl.SSL_VERIFYHOST, 2)
	# r.setopt(pycurl.CAINFO, certFile)
	# r.setopt(pycurl.URL, URL)
	return r

class scrapingTool(object):
	def __init__(self):
		self.headers = {}
		self.r = setupResp()

	def setCertFile(self, certFile):
		self.r.setopt(pycurl.CAINFO, certFile)

	def close(self):
		self.r.close()

	def header_function(self, header_line):
		# HTTP standard specifies that headers are encoded in iso-8859-1.
		# On Python 3, decoding step is required.
		header_line = header_line.decode('iso-8859-1')

		# Header lines include the first status line (HTTP/1.x ...).
		# We are going to ignore all lines that don't have a colon in them.
		# This will botch headers that are split on multiple lines...
		if ':' not in header_line:
			return

		# Break the header line into header name and value.
		name, value = header_line.split(':', 1)

		# Remove whitespace that may be present. Header lines include the trailing newline, and there may be whitespace around the colon.
		name = name.strip()
		value = value.strip()

		name = name.lower()  # Header names are case insensitive. Still, force the name to lowercase here. For some reason.

		# Now we can actually record the header name and value.
		# Note: this only works when headers are not duplicated, see below.
		self.headers[name] = value

	def getBody(self, url):
		headers = self.headers
		r = self.r

		if url in [None, ""]:
			raise ("No url to scrape.")  # Should never occur, but just to be safe
		r.setopt(pycurl.URL, url)

		buffer = BytesIO()
		r.setopt(r.WRITEFUNCTION, buffer.write)
		r.setopt(r.HEADERFUNCTION, self.header_function)
		r.perform()
		# r.close()

		# Figure out what encoding was sent with the response, if any. Check against lowercased header name.
		encoding = None
		if 'content-type' in headers:
			content_type = headers['content-type'].lower()
			match = re.search('charset=(\S+)', content_type)
			if match:
				encoding = match.group(1)
				# print('Decoding using', encoding)
		if encoding is None:
			# Default encoding for HTML is iso-8859-1.
			# Other content types may have different default encoding, or in case of binary data, may have no encoding at all.
			encoding = 'iso-8859-1'
			# print('Assuming encoding is', encoding)

		body = buffer.getvalue()
		# Decode using the encoding we figured out.
		# print(body.decode(encoding))

		return body.decode(encoding)

scraper = scrapingTool()

def getScraper():
	""" Use getScraper to get global access to shared instance of scrapingTool, 'scraper' """
	# if not scraper: print('scraper does not exist')
	# elif scraper: print('scraper exists')
	return scraper