This is the reference for the .vance format.
vance files are encoded in latin-1.
#Spaces are *only* added for readability.

0x55 VABIN is the magic number.

0xF0 is the Header Checksum.

Right after the Header Checksum there is 0x00 and then there is a single byte representing the version number.

0x00 0x90 0x9F 0xF9 marks the beginning and end of the metatags.

0xE5 0x6E Separates each metatag.

0xFF 0x99 0xAB marks the beginning and end of the data.

0xF7 0x00 0xBB separates each data key.

0xBF separates the data key from its value.
