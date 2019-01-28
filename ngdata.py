from pathHelpers import validateFile
from scraper import *

if __name__ != "__main__":  # If running test.py, and I guess anything else except this directly...
	from example.pageHandlers import handleURL
else:
	from pageHandlers import handleURL

# sep = "\n===============================================================\n"
emptyList = [None, [], '', ['']]
scraper = getScraper()
out = None

def output(dest, text):
	if dest in [None, '']:
		print(text.encode("utf-8"))
	else:
		# Leave the file open until explicitly closed.
		# This is so that the file will be appended to while the program is
		# already running, but will be overwritten upon starting it again

		# Replaced 'with open(...)' with a global, which will hopefully also be replaced eventually...
		# with open(dest, "a+", encoding = "utf-8") as out:
		global out
		if out is None:
			out = open(dest, "w+", encoding = "utf-8")
			out.write('[\n')
		out.write(text)

def start(outputFile, src, certFile):
	# TODO: Make this return something to indicate success or (reason for) failure
	scraper.setCertFile(certFile)
	# from pycurl import error
	# import json
	# for v in src[1]:
	# 	try:
	# 		data = getScraper().getBody(v)
	# 		output(outputFile, json.dumps(data))
	# 	except error:
	# 		output(outputFile, json.dumps(v))

	if src[0] == 0:  # src can be used as is
		URL = src[1]
		# Replaced: Incorporated the inclusion of the link into the handler as well
		# output(outputFile, 'link:\t' + URL[0])
		result = handleURL(URL[0])
		output(outputFile, result)

		for var in URL[1:]:
			# Replaced: Incorporated the inclusion of the link into the handler as well
			# output(outputFile, sep + "link:\t" + var)
			result = handleURL(var)
			output(outputFile, result)
	else:  # src is in a file, and must be retrieved for use
		# TODO!!
		print("This program does not currently handle src from a file. For now, please try redirecting the file into the program call.")

def fin():
	scraper.close()  # explicitly close connection when finished
	if out is not None:
		out.write('{"null":""}\n]')
		out.close()

if __name__ == "__main__":
	import argparse

	def handleArgs():
		parser = argparse.ArgumentParser(description = 'Scrape certain types of urls.')
		parser.add_argument(
				'-o', action = 'store', nargs = '?', default = '', type = str, const = 'outputFile.txt',
				metavar = 'outputFile', dest = 'outputFile',
				help = 'The absolute path to a file where the processed information should be sent. With \'-o\', if no path is specified, send output to \'./outputFile.txt\'. If \'-o\' is not specified, output is printed to stdout.'
		)
		parser.add_argument(
				'-c', action = 'store', nargs = '?', default = None, type = str, metavar = 'certFile', dest = 'certFile',
				help = 'Full path to certificate authority file'
		)
		inputSrc = parser.add_mutually_exclusive_group(required = True)
		inputSrc.add_argument(
				'-u', action = 'store', nargs = argparse.REMAINDER, default = '', type = str, metavar = 'urls', dest = 'urls',
				help = 'One or more URLs to scrape from, separated by a space.'
				# '-u', action = 'store', nargs = '*', default = '', type = str, metavar = 'urls', dest = 'urls',
				# help = 'One or more URLs to scrape from, separated by a space.'	#requires python 3.7 for ArgumentParser.parse_intermixed_args
		)
		inputSrc.add_argument(
				'-i', action = 'store', nargs = 1, default = '', type = str, metavar = 'inputFile', dest = 'inputFile',
				help = 'The absolute path to a file containing URLs to scrape, separated by a space.'  # or newlines?
		)
		# return parser.parse_intermixed_args()	requires python 3.7
		return parser.parse_args()

	def run():
		args = handleArgs()
		# if args.urls : print ('args.urls non-empty; contains: "' + str(args.urls)+"'")
		if (args.urls not in [None, '']):
			src = [0, args.urls]
		# print("\033[31murls="+args.urls+"\033[0m")
		else:
			src = [1, args.inputFile]
		# print("\033[31minputFile="+args.inputFile[0]+"\033[0m")

		certFile = validateFile(args.certFile)
		outputFile = validateFile(args.outputFile) if args.outputFile != '' else ''

		# Because argparse.REMAINDER can be empty, check it, and exit if it is.
		if (src[1] in emptyList):
			# the case for [''] solves the issue of dealing with an input of '' or ""
			print("No urls to scrape. Exiting...")
			exit()
		# if not(src[1]): print("src[1] is False-y"); exit();
		# print ("\033[31m"+repr(src[1])+"\033[0m")
		# print ("T" if src[1] in ['', "\'\'", '\"\"', '\'\'', "'\'", "\''", [], "[]", ["\'\'"]] else "F")
		# print ("\033[32m"+str(src[1])+"\033[0m")
		# print(str(type(str(src[1]))))
		# print ("len(src[1])= " + str(len(str(src[1]))))
		# for v in str(src) : print("\033[33m"+str(v)+"\033[0m")
		# print(str(src))
		# print(str(src[1]))

		# print('output to:'+repr(args.outputFile))
		# print('src = ' + repr(src))
		# print('certfile = ' + certFile)
		start(outputFile, src, certFile)

	run()
	fin()