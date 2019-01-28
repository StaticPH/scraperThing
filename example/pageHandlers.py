import re
from scraper import getScraper

filler = '+++++++++++++++++++++++\n'
imageLinkSuffix = ['.png', '.jpg', '.gif', '.jpeg']
# knownDead = re.compile('')
noDetailList = []  # If ALL links to a site should not be scraped, but simply left as is, put the domain (with url prefix/sub-domain!) into this list

class giphyProc(object):
	""" Handle all links to giphy.com """

	def __init__(self):
		self.regexCut = re.compile("/giphy\.(png|jpg|gif|jpeg).*", re.I)

	@staticmethod
	def convertDirect(url):
		"""
			Converts a link to a media source file into a link to a page about that media.
			Example: media.giphy.com/media/someString/giphy.gif --> giphy.com/gifs/someString
		"""
		# return url.replace('media.' ,'').replace('giphy.gif' ,'').replace('media/', 'gifs/')
		# return self.regexCut.sub("", url.replace('media.' ,'').replace('media/', 'gifs/'))
		tmp = url.split('media', 2)
		tmp = tmp.pop()
		tmp = tmp.split('/')[1]
		return 'https://giphy.com/gifs/' + tmp

	@staticmethod
	def badMatch(url):
		return '{\n"invalid_match_for_handler": "' + url + '"\n},\n'

	@staticmethod
	def grabTags(data):
		return '\"' + (data.split(', GIF, Animated GIF">'))[0] + '\",\n\t\t'

	@staticmethod
	def clean(data):
		b = (data.split('"@id": '))[1]
		# b = (data.replace('"@id": '))[1]
		b = (b.split('"publisher'))[0]
		b1 = (b.split('}'))[0].strip()
		b2 = (b.split('"headline":'))[1]
		return '"url": ' + b1 + ',\n\t\t"headline":' + b2

	def go(self, url):
		if url.find('/media/') == -1 and url.find('/gifs/') == -1:
			return self.badMatch(url)

		# if (url.endswith(tuple(imageLinkSuffix))) or url.find('media') != -1:
		if url.find('media') != -1:
			if url.count('media') < 2:
				return self.badMatch(url)
			url = self.convertDirect(url)  # ;print("url fixed to : " + url)
		# else: print("url needed no fixing.")

		data = getScraper().getBody(url)
		data = (data.split('<style>body'))[0]
		data = (data.split('keywords" content="'))[1]
		data = '{\n\t\t"keywords": ' + self.grabTags(data) + self.clean(data).strip().rstrip(',') + '\n},\n'
		# data=b + '}'
		# data=a+b.strip() + '\n}'
		return data

giphy = giphyProc()

def unknownHandle(url):
	""" When encountering a url that does not have a specific handler, use this. """
	return (
			'{\n\t\t"unknownHandle": "Could not find an appropriate handler for url",' +
			'\n\t\t"url": "' + url + '"\n},\n'
			)

def deadHandle(url):
	""" When handling a link to a site known to be dead, label it with "DEAD LINK: " to indicate that"""
	return '{\n\t\t"DEAD_LINK": "' + url + '"\n},\n'

def noScrape(url):
	""" For urls that should not be scraped, return the url as is, formatted similarly to json """
	return ('{\n\t\t"url": "' + url + '"\n},\n')

def handleImageUrlFallback(url):
	""" When encountering a url known to be for a single image, return the url as is, formatted similarly to json """
	return noScrape(url)

def selectHandler(url):
	""" Trim protocol and www. prefixes if they exist, then determine and return the proper handler function to use for url """
	tmp = url.split('://', 1)  # Operate under the assumption that protocol exists at most once per url
	tmp = tmp.pop()  # Whether the original url had a protocol or not, get the url without it. Using pop prevents any errors if tmp only has one index.
	tmp = tmp.split('www.', 1)  # Assume that 'www.' will also occur no more than once in a given url
	url = tmp.pop()  # Whether the original url started with 'www.' or not, get the url without it.

	# if (re.match(knownDead, url) is not None):
		# If the url matches the regular expression for known dead websites
		# return deadHandle
	if url.startswith(tuple(noDetailList)):
		# If the url's 'prefix+domain' is in the list of 'prefix.domain's not to scrape.
		return noScrape
	elif url.startswith(('giphy.com', 'media.giphy.com')):
		return giphy.go
	elif url.endswith(tuple(imageLinkSuffix)):
		# If the url suffix is a standard image format, it's almost certainly an image.
		# If not handled specially by the handler for its domain, it should be handled by the fallback image handler.
		return handleImageUrlFallback
	else:
		return unknownHandle

def handleURL(url):
	""" Select the handler for a url and return the result of the handling. """
	return (selectHandler(url))(url)