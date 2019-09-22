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
import os, json, json.scanner

from vfjLib.object import attribdict
from vfjLib.parser import vfj_decoder, vfj_encoder

__version__ = '0.1.7'

# - Objects -----------------------------------------
class vfjFont(attribdict):
	def __init__(self, vfj_path):
		self._vfj_read(vfj_path)

	def __repr__(self):
		return '<%s name=%s, masters=%s, glyphs=%s, version=%s>' %(self.__class__.__name__, self.font.info.tfn, len(self.font.masters), self.font.glyphsCount, self.font.info.version)

	def _vfj_read(self, vfj_path):
		self.update(json.load(open(vfj_path, 'r'), cls=vfj_decoder))

	def _vfj_write(self, vfj_path):
		json.dump(open(vfj_path, 'w'), cls=vfj_encoder)

	def split(self, path):
		split = self.font
		root = os.path.join(path, self.font.info.tfn)
		os.mkdir(root)
		agg = attribdict()

		for key, value in split.items():
			if isinstance(value, dict):
				json.dump(value, open(os.path.join(root, key), 'w'), cls=vfj_encoder)
			
			elif isinstance(value, list):
				subfolder = os.path.join(root, key)
				os.mkdir(subfolder)

				for item_index in range(len(value)):
					json.dump(value[item_index], open(os.path.join(root, key + str(item_index)), 'w'), cls=vfj_encoder)
			else:
				agg[key] = value

		json.dump(agg, open(os.path.join(root, 'more'), 'w'), cls=vfj_encoder)




