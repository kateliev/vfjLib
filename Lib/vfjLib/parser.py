# encoding:	utf-8
# ----------------------------------------------------
# MODULE: 	Parsers | vfjLib
# ----------------------------------------------------
# (C) Vassil Kateliev, 2019  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# NOTE:		Module is kept Python 2 and 3 compatible!

# No warranties. By using this you agree
# that you use it at your own risk!

from __future__ import absolute_import, unicode_literals, print_function
import json, json.scanner
from vfjLib.object import attribdict

__version__ = '0.1.8'

# - Parsers -----------------------------------------
# -- Vector Font JSON (VFJ)
class vfj_decoder(json.JSONDecoder):
	def __init__(self, *args, **kwdargs):
		super(vfj_decoder, self).__init__(*args, **kwdargs)
		self.__parse_object = self.parse_object
		self.parse_object = self._parse_object
		self.scan_once = json.scanner.py_make_scanner(self)
		self.__tree_class = attribdict
	
	def _parse_object(self, *args, **kwdargs):
		result = self.__parse_object(*args, **kwdargs)
		tree_obj = self.__tree_class(result[0])
		tree_obj.lock() # Lock the tree - no further editing allowed
		return tree_obj, result[1]

class vfj_encoder(json.JSONEncoder):
	def __init__(self, *args, **kwdargs):
		super(vfj_encoder, self).__init__(*args, **kwdargs)
	
	def default(self, obj):
		return super(vfj_encoder, self).default(obj)

# -- File and folder names ----------------------------
# Note: Parts of the File and folder names parser are based on ufoLib/filenames.py
# Note: Copyright (c) 2005-2018, The RoboFab Developers: Erik van Blokland, Tal Leming, Just van Rossum

# --- List updated accoridng to https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
illegalCharacters = r'\' * + / : < > ? [ \ ] | \0'.split(' ')
illegalCharacters += [chr(i) for i in range(1, 32)]
illegalCharacters += [chr(0x7F)]
reservedFileNames += 'CLOCK$ A:-Z: CON PRN AUX NUL COM1 COM2 COM3 COM4 COM5 COM6 COM7 COM8 COM9 LPT1 LPT2 LPT3 LPT4 LPT5 LPT6 LPT7 LPT8 LPT9'.lower().split(' ')
maxFileNameLength = 255

def string2filename(string, suffix):
	# - Initial test
	if not isinstance(string, str):	raise ValueError('The value for string must be type(str)!')

	# - Replace an initial period with an _
	if string[0] == '.': string = '_' + string[1:]
	
	# - Filter the user name
	filtered_string = []
	for character in string:
		
		if character in illegalCharacters: # replace illegal characters with _
			character = '_'
		
		elif character != character.lower(): # add _ to all non-lower characters
			character += '_'

		filtered_string.append(character)

	string = ''.join(filtered_string)

	# - Clip to maxFileNameLength
	string = string[:maxFileNameLength - len(suffix)]

	# - Test for illegal files names
	parts = []
	for part in string.split('.'):
		if part.lower() in reservedFileNames:
			part = '_' + part
		parts.append(part)

	string = '.'.join(parts)

	filename = string + suffix
	return filename
