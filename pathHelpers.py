import os.path

class InvalidPathTarget(OSError):
	"""Exception raised when looking for a type of file (e.g. symlink, directory, etc.) and finding something else"""

	def __init__(self, message):        self.message = message

def fixPath(path):
	# Handle any would-be escape characters in the path string
	path = os.path.normpath(repr(path).replace('\\', '/'))

	# Trim off the quotes added by repr
	if (path.startswith("'") and path.endswith("'")) or (path.startswith('"') and path.endswith('"')):
		path = path[1:-1]

	# Apparently you can still check if a path is absolute even when the path doesnt actually exist. Not sure how I feel about that...
	if os.path.isabs(path) == False:
		path = os.path.abspath(path)

	return path

def validateFile(path):
	path = fixPath(path)

	# If path exists, but is not a file, cry foul. Technically, it shouldn't need to explicitly check for existence, but shouldn't hurt.
	if (os.path.exists(path)) and (os.path.isfile(path) == False):
		raise InvalidPathTarget("Location indicated by  `" + path + "` is not a file.")

	return path