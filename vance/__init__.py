from traceback import format_exc
import logging
from .classes import *
import warnings
import sys


VERSION_NUMBER = "b1.0"

DO_LOGGING = True

DEFAULT_META_TAGS = { #Use these if you wish to change metatags
	"pyonly": False,
	"allow-old-version": True,
	"file-name": "NO_FILE_NAME_GIVEN"
}

###Sets up logging
if DO_LOGGING:
	loghandler = logging.FileHandler("vance.log")
	loghandler.setLevel(logging.DEBUG)
	logfmt = logging.Formatter(fmt="%(asctime)s: %(levelname)s - %(message)s \n")
	loghandler.setFormatter(logfmt)
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(loghandler)
###aaaaaaaaaaaaaaa
	

def createVanceData(metatags=DEFAULT_META_TAGS, data={}):
	"""Function that returns a VanceFileData object. metatags should normally be left blank and data should 	
	be the dict that you want to store.""" 
	return VanceFileData(metatags, data, VERSION_NUMBER)
	
def dump(obj, fp, fname=None):
	"""Dumps the VanceFileData object to fp. fp should accept byes objects. fname shoukd be the file name 
	(optional). Automatically encodes data."""
	obj.encode()
	obj.writeToFile(fp, name=fname)
	
def parseFileData(content):
	"""Parses content (bytes object) into a VanceFileData object. Returns VanceFileData object."""
	logger.debug(f"began parsing file (content: {content.decode('latin-1')})".encode("latin-1"))
	obsoleteFile = False
	if not content.startswith(b"\x55VABIN\xF0\x00"):
		raise VanceError("Either the magic number or Header Checksum is missing.")
	logger.debug("magic number and header checksum are both present")
	fileVersion = content.split(b"\x00")[1]
	logger.debug(f"file's version is {fileVersion}")
	if fileVersion != bytes(VERSION_NUMBER, encoding="ascii"):
		obsoleteFile = True
	metaTags = content.split("\x00\x90\x9F\xF9".encode("latin-1"))[1]
	logger.debug(f"began parsing metatags: {metaTags.decode('latin-1')}".encode("latin-1"))
	metaTagsArr = metaTags.split("\xE5\x6E".encode("latin-1"))
	metaTagsArr.pop(0)
	logger.debug(f"metaTagsArr = {metaTagsArr}")
	metaTags = {}
	for x in metaTagsArr:
		currentTag = x.split(b"\xFA")
		logger.debug(f"got tag {currentTag}\n\n")
		metaTags[currentTag[0].decode("latin-1")] = currentTag[1].decode("latin-1")
	if metaTags["allow-old-version"] == "True" and obsoleteFile==True:
		warnings.warn(f"vance file with name {metaTags['file-name']} is using a different version: {fileVersion.decode()}")
	elif metaTags["allow-old-version"] == "False" and obsoleteFile==True:
		raise VanceError(f"{metaTags['file-name']} is using a different version: {fileVersion}")
	data = content.split(b"\xFF\x99\xAB")[1]
	dataArr = data.split(b"\xF7\x00\xBB")
	dataArr.pop(0)
	dataDict = {}
	for x in dataArr:
		keyVal = x.split(b"\xBF")
		dataDict[keyVal[0].decode("latin-1")] = keyVal[1].decode("latin-1")
	return createVanceData(metaTags, dataDict)
	
def load(fp):
	"""Loads a Vance file and returns its data attribute. fp should be the file to read from and should 
	support bytes."""
	try:
		with fp:
			obj = parseFileData(fp.read())
		return obj.data
	except:
		logger.error(format_exc())
		raise sys.exc_info()[1]
		
