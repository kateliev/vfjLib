# encoding:	utf-8
# ----------------------------------------------------
# MODULE: 	Objects | vfjLib
# ----------------------------------------------------
# (C) Vassil Kateliev, 2019  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# NOTE:		Module is kept Python 2 and 3 compatible!

# No warranties. By using this you agree
# that you use it at your own risk!

from __future__ import absolute_import, unicode_literals, print_function
from collections import defaultdict

__version__ = '0.1.7'

# - Objects ------------------------------------------
class attribdict(defaultdict):
	'''	Default dictionary where keys can be accessed as attributes	'''
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

	def __delattr__(self, name):
		try:
			return object.__delattr__(self, name)
		except AttributeError:
			return self.pop(name, None)
					
	def __repr__(self):
		return '<%s: %s>' %(self.__class__.__name__, len(self.keys()))

	def dir(self):
		tree_map = ['   .%s\t%s' %(key, type(value)) for key, value in self.items()]
		print('Attributes (Keys) map:\n%s' %('\n'.join(tree_map).expandtabs(30)))

	def factory(self, factory_type):
		self.default_factory = factory_type

	def lock(self):
		self.default_factory = None

	def extract(self, search):
		'''Pull all values of specified key (search)'''
		array = []

		def extract_helper(obj, array, search):
			if isinstance(obj, dict):
				for key, value in obj.items():
					if isinstance(value, (dict, list)):
						extract_helper(value, array, search)

					elif key == search:
						array.append(value)

			elif isinstance(obj, list):
				for item in obj:
					extract_helper(item, array, search)

			return array

		results = extract_helper(self, array, search)
		return results

	def where(self, search):
		'''Pull all objects that contain specified value (search)'''
		array = []
		
		def where_helper(obj, array, search):
			if isinstance(obj, dict):
				for key, value in obj.items():
					if isinstance(value, (dict, list)):
						where_helper(value, array, search)

					elif value == search:
						array.append(obj)

			elif isinstance(obj, list):
				for item in obj:
					where_helper(item, array, search)

			return array

		results = where_helper(self, array, search)
		return results
