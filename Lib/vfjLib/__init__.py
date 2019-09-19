# encoding:	utf-8
# ----------------------------------------------------
# MODULE: 	vfjLib
# DESC:		A low-level VFJ reader and writer.
# ----------------------------------------------------
# (C) Vassil Kateliev, 2019  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# NOTE:		Module is kept Python 2 and 3 compatible!

# No warranties. By using this you agree
# that you use it at your own risk!

from __future__ import absolute_import, unicode_literals, print_function

import os
import json, json.scanner
from collections import defaultdict


# - Init ---------------------------------------------
__version__ = '0.1.5'

# - Classes ------------------------------------------
class attribdict(defaultdict):
	'''
	Default dictionary where keys can be accessed as attributes
	----
	Adapted from JsonTree by Doug Napoleone: https://github.com/dougn/jsontree
	'''
	def __init__(self, *args, **kwdargs):
		super(attribdict, self).__init__(attribdict, *args, **kwdargs)

	def __getattribute__(self, name):
		try:
			return object.__getattribute__(self, name)
		except AttributeError:
			return self[name]
		
	def __setattr__(self, name, value):
		if name in self.keys():
			self[name] = value
			return value
		else:
			object.__setattr__(self, name, value)
					
	def __repr__(self):
		return '<%s: %s>' %(self.__class__.__name__, len(self.keys()))

	def help(self):
		tree_map = ['   .%s\t%s' %(key, type(value)) for key, value in zip(self.keys(), self.values())]
		print('Attributes/Keys:\n%s' %('\n'.join(tree_map).expandtabs(30)))

	def factory(self, factory_type):
		self.default_factory = factory_type

	def lock(self):
		self.default_factory = None

# -- Parsers
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

# -- Objects
class vfjFont(object):
	def __init__(self, vfj_path):
		self._path, self._file = os.path.split(vfj_path)
		self.data = self._vfj_read(vfj_path)

	def __repr__(self):
		return '<%s name=%s, masters=%s, glyphs=%s, version=%s>' %(self.__class__.__name__, self.data.font.info.tfn, len(self.data.font.masters), self.data.font.glyphsCount, self.data.font.info.version)

	def _vfj_read(self, vfj_path):
		return json.load(open(vfj_path), cls=vfj_decoder)

	def _vfj_write(self, vfj_path):
		return json.dump(open(vfj_path), cls=vfj_encoder)


