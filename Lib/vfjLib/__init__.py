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

from __future__ import absolute_import, print_function, unicode_literals

import json
import json.scanner
import os

from vfjLib.object import attribdict
from vfjLib.parser import vfj_decoder, vfj_encoder

__version__ = '0.1.9'

# - Deafaults --------------------------------------
vfj_version = 8
vfj_split_suffix = 'json'

# - Objects -----------------------------------------
class vfjFont(attribdict):
	def __init__(self, vfj_path=None):
		self.vfj_path = vfj_path		
		if self.vfj_path is not None: self._vfj_read(self.vfj_path)

	def __repr__(self):
		if len(self.keys()):
			return '<%s name=%s, masters=%s, glyphs=%s, version=%s>' %(self.__class__.__name__, self.font.info.tfn, len(self.font.masters), self.font.glyphsCount, self.font.info.version)
		else:
			return '<%s name=None, masters=None, glyphs=None, version=None>' %self.__class__.__name__

	def _vfj_read(self, vfj_path):
		self.vfj_path = vfj_path
		self.update(json.load(open(vfj_path, 'r'), cls=vfj_decoder))

	def _vfj_write(self, vfj_path):
		json.dump(self, open(vfj_path, 'w'), cls=vfj_encoder)

	def _vfj_split(self, split_path):
		split = self.font
		root = os.path.join(split_path, self.font.info.tfn)
		os.mkdir(root)
		agg = attribdict()

		for key, value in split.items():
			if isinstance(value, dict):
				item_name ='%s.%s'%(key, vfj_split_suffix)
				json.dump(value, open(os.path.join(root, item_name), 'w'), cls=vfj_encoder)

			elif isinstance(value, list):
				subfolder = os.path.join(root, key)
				os.mkdir(subfolder)

				for item_index in range(len(value)):
					item_name ='%s.%s'%(key, item_index)

					if value[item_index].has_key('name'):
						item_name ='%s.%s'%(value[item_index].name, vfj_split_suffix)
					elif value[item_index].has_key('tfn'):
						item_name ='%s.%s'%(value[item_index].tfn, vfj_split_suffix)
					elif value[item_index].has_key('fontMaster'):
						item_name ='%s.%s'%(value[item_index].fontMaster.name, vfj_split_suffix)

					json.dump(value[item_index], open(os.path.join(subfolder, item_name), 'w'), cls=vfj_encoder)
			else:
				agg[key] = value

		json.dump(agg, open(os.path.join(root, 'more.json'), 'w'), cls=vfj_encoder)

	def _vfj_join(self, join_path):
		from vfjLib.object import attribdict
		
		root = join_path
		self['font'] = attribdict()
		self['version'] = vfj_version
		
		for dirName, subdirList, fileList in os.walk(root, topdown=True):
			if dirName == root:
				for key in subdirList:
					self.font[key] = []

				for fileName in fileList:
					self.font[fileName.split('.')[0]] = attribdict(json.load(open(os.path.join(dirName, fileName), 'r'), cls=vfj_decoder))
			else:
				if os.path.split(dirName)[1] in self.font.keys():
					for fileName in fileList:
						self.font[os.path.split(dirName)[1]].append(attribdict(json.load(open(os.path.join(dirName, fileName), 'r'), cls=vfj_decoder)))

						# so far so good! fix the more.json import


	def save(self, vfj_path=None, split=False):
		if vfj_path is None: 
			vfj_path = self.vfj_path

		if not slplit:
			self._vfj_write(vfj_path)
		else:
			self._vfj_split(vfj_path)

	def open(self, vfj_path=None, join=False):
		if not join:
			self._vfj_read(vfj_path)
		else:
			self._vfj_join(vfj_path)
