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

__version__ = '0.1.7'

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
