class VanceError(Exception):
	pass
	
class VanceFileData:
	"""Class that represents a Vance file. Should be created using createVanceData()."""
	def __init__(self, metatags, data, version):
		self.metatags = metatags
		self.version = version
		self.data = data
		self.bcontent = b"\x55VABIN\xF0\x00" + bytes(self.version, encoding="latin-1") +  b"\x00\x90\x9F\xF9"
		self.encoded = False
		
	def encodeMetaTags(self):
		for x in self.metatags:
			self.bcontent += b"\xE5\x6E" + bytes(str(x), encoding="latin-1") + b"\xFA" + bytes(str(self.metatags[x]), encoding="latin-1")
		self.bcontent += b"\x00\x90\x9F\xF9"
			
	def encodeData(self): 
		self.bcontent += b"\xFF\x99\xAB"
		for x in self.data:
			self.bcontent += b"\xF7\x00\xBB" + bytes(str(x), encoding="latin-1") + b"\xBF" + bytes(str(self.data[x]), encoding="latin-1")
		self.bcontent += b"\xFF\x99\xAB"
		
	def encode(self):
		"""Encodes all data and metatags to self.bcontent by calling both self.encodeMetaTags and 
		self.encodeData."""
		if not self.encoded:
			self.encodeMetaTags()
			self.encodeData()
			self.encoded = True
		else:
			self.__init__(self.metatags, self.data, self.version)
			self.encode()
		
	def writeToFile(self, fp, name=None):
		"""Writes self.bcontent to fp. fp must be opened in a mode that supports writing bytes. name sets the 
		file-name metatag and defaults to None (if left at None, will default to name already set in 
		metatags.)"""
		if name==None:
			name = self.metatags["file-name"]
		self.metatags["file-name"] = name
		with fp:
			self.encode()
			fp.write(self.bcontent)
			
	def __str__(self):
		return self.bcontent.decode("latin-1")
