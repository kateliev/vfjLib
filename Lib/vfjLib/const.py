# encoding:	utf-8
# ----------------------------------------------------
# MODULE: 	Constants | vfjLib
# ----------------------------------------------------
# (C) Vassil Kateliev, 2019  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# NOTE:		Module is kept Python 2 and 3 compatible!

# No warranties. By using this you agree
# that you use it at your own risk!

from __future__ import unicode_literals

__version__ = '0.1.0'

# - VFJ Specific -------------------------------------
class cfg_vfj(object):
	def __init__(self):
		self.delimiter = '.'
		self.vfj_version_value = 8 			# Current VFJ version according to FL
		self.vfj_values_fileName = 'values' # Special filename to hold all standalone values

		self.major_split_suffix = 'svfj'
		self.minor_split_suffix = 'json'
		self.glyph_split_suffix = self.minor_split_suffix
		self.feaure_split_suffix = self.minor_split_suffix
		self.master_split_suffix = self.minor_split_suffix

# - File Specific ------------------------------------
class cfg_filename(object):
	def __init__(self):
		# - List updated according to https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
		self.illegal = r'\' * + / : < > ? [ \ ] | \0'.split(' ')
		self.illegal += [chr(i) for i in range(1, 32)]
		self.illegal += [chr(0x7F), ' ']		
		
		# - List updated according to https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
		self.reserved = 'CLOCK$ A:-Z: CON PRN AUX NUL COM1 COM2 COM3 COM4 COM5 COM6 COM7 COM8 COM9 LPT1 LPT2 LPT3 LPT4 LPT5 LPT6 LPT7 LPT8 LPT9'.lower().split(' ')
		
		# - Maximum file length
		self.max_len = 255 

		# - Special character to fix filenames with
		self.special = '_'
		self.delimiter = '.'