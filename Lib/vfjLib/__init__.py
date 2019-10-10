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

from vfjLib.const import cfg_vfj
from vfjLib.object import attribdict
from vfjLib.parser import vfj_decoder, vfj_encoder, string2filename

__version__ = '0.2.7'

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
		json.dump(self, open(vfj_path, 'w'), cls=vfj_encoder, sort_keys=True, indent=4)

	def _vfj_split(self, split_path):

		cfg_file = cfg_vfj()
		split = self.font

		if os.path.isfile(split_path): 
			root = '%s.%s' %(os.path.splitext(split_path)[0], cfg_file.major_split_suffix)
		else:
			root = os.path.join(split_path, string2filename(self.font.info.tfn, cfg_file.major_split_suffix))

		os.mkdir(root)
		agg = attribdict()

		for key, value in split.items():
			if isinstance(value, dict):
				item_name ='%s.%s'%(key, cfg_file.minor_split_suffix)
				json.dump(value, open(os.path.join(root, item_name), 'w'), cls=vfj_encoder, sort_keys=True, indent=4)

			elif isinstance(value, list):
				subfolder = os.path.join(root, key)
				os.mkdir(subfolder)

				for item_index in range(len(value)):
					item_name = string2filename('%s.%s' %(key, item_index), cfg_file.feaure_split_suffix)

					if value[item_index].has_key('name') and not value[item_index].has_key('tsn'):
						item_name = string2filename(value[item_index].name, cfg_file.glyph_split_suffix, True)
					
					elif value[item_index].has_key('name'):
						item_name = string2filename(value[item_index].name, cfg_file.glyph_split_suffix)

					elif value[item_index].has_key('tfn'):
						item_name = string2filename(value[item_index].tfn, cfg_file.master_split_suffix)

					elif value[item_index].has_key('fontMaster'):
						item_name = string2filename(value[item_index].fontMaster.name, cfg_file.master_split_suffix)

					json.dump(value[item_index], open(os.path.join(subfolder, item_name), 'w'), cls=vfj_encoder, sort_keys=True, indent=4)
			else:
				agg[key] = value

		json.dump(agg, open(os.path.join(root, string2filename(cfg_file.vfj_values_fileName, cfg_file.minor_split_suffix)), 'w'), cls=vfj_encoder, sort_keys=True, indent=4)

	def _vfj_join(self, join_path):
		from vfjLib.object import attribdict
		
		cfg_file = cfg_vfj()
		root = join_path
		self['version'] = cfg_file.vfj_version_value
		self['font'] = attribdict()
		
		for dirName, subdirList, fileList in os.walk(root, topdown=True):
			if dirName == root:
				for key in subdirList:
					self.font[key] = []

				for fileName in fileList:
					if fileName == '%s.%s' %(cfg_file.vfj_values_fileName, cfg_file.minor_split_suffix):
						self.font.update(json.load(open(os.path.join(dirName, fileName), 'r'), cls=vfj_decoder))
					else:
						self.font[fileName.split('.')[0]] = json.load(open(os.path.join(dirName, fileName), 'r'), cls=vfj_decoder)

			else:
				if os.path.split(dirName)[1] in self.font.keys():
					for fileName in fileList:
						self.font[os.path.split(dirName)[1]].append(json.load(open(os.path.join(dirName, fileName), 'r'), cls=vfj_decoder))

		self._vfj_rebuild_glyph_array()
		self.font.lock()

	def _vfj_rebuild_glyph_array(self):
		glyph_base, glyph_ref, glyph_comp, glyph_other = [], [], [], []

		for glyph in self.font.glyphs:
			if glyph.contains('elementData', unicode): 
				glyph_ref.append(glyph)
			
			elif glyph.contains('component'): 
				glyph_comp.append(glyph)
			
			elif glyph.contains('elementData', dict):
				if glyph not in glyph_ref and glyph not in glyph_comp:
					glyph_base.append(glyph)
			else:
				glyph_other.append(glyph)

		self.font.glyphs = glyph_base + glyph_ref + glyph_comp + glyph_other
		self.font.glyphsCount = len(self.font.glyphs)		

	def save(self, vfj_path=None, split=False):
		if vfj_path is None: 
			vfj_path = self.vfj_path

		if not split:
			self._vfj_write(vfj_path)
		else:
			self._vfj_split(vfj_path)

	def open(self, vfj_path=None, join=False):
		if not join:
			self._vfj_read(vfj_path)
		else:
			self._vfj_join(vfj_path)
