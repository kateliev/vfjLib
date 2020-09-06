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

__version__ = '0.2.1'

# - Objects ------------------------------------------
class dictextractor:
	'''A collection of dicionary value extractors'''

	@staticmethod
	def extract(obj, search):
		'''Pull all values of specified key (search)
		
		Attributes:
			search (Str): Search string

		Returns:
			generator
		'''
		
		def extract_helper(obj, search):
			if isinstance(obj, dict):
				for key, value in obj.items():
					if key == search:
						yield value
					else:	
						if isinstance(value, (dict, list)):
							for result in extract_helper(value, search):
								yield result

			elif isinstance(obj, list):
				for item in obj:
					for result in extract_helper(item, search):
						yield result

		return extract_helper(obj, search)

	@staticmethod
	def find(obj, search, search_type=None):
		'''Pull all objects that contain keys of specified search.
		
		Attributes:
			search (Str): Search string
			search_type (type) : Value type
		Returns:
			generator
		'''
		def isisntance_plus(entity, test_type):
			if test_type is not None:
				return isinstance(entity, test_type)
			else:
				return True

		def where_helper(obj, search):
			if isinstance(obj, dict):
				for key, value in obj.items():
					if key == search and isisntance_plus(value, search_type):
						yield obj
					else:	
						if isinstance(value, (dict, list)):
							for result in where_helper(value, search):
								yield result

			elif isinstance(obj, list):
				for item in obj:
					for result in where_helper(item, search):
						yield result

		return where_helper(obj, search)

	@staticmethod
	def where(obj, search_value, search_key=None):
		'''Pull all objects that contain values of specified search.
		
		Attributes:
			search_value (Str): Search value
			search_key (Str) : Search for specific key that contains above value
		Returns:
			generator
		'''
		def eq_plus(test, pass_test):
			if pass_test is not None:
				return test
			else:
				return True

		def where_helper(obj, search_value):
			if isinstance(obj, dict):
				for key, value in obj.items():
					if value == search_value and eq_plus(key==search_key, search_key):
						yield obj
					else:	
						if isinstance(value, (dict, list)):
							for result in where_helper(value, search_value):
								yield result

			elif isinstance(obj, list):
				for item in obj:
					for result in where_helper(item, search_value):
						yield result

		return where_helper(obj, search_value)

	@staticmethod
	def contains(obj, search, search_type=None):
		'''Does the object contain ANY value or nested object with given name (search)
		
		Attributes:
			search (Str): Search string
			search_type (type) : Value type

		Returns:
			Bool
		'''
		def isisntance_plus(entity, test_type):
			if test_type is not None:
				return isinstance(entity, test_type)
			else:
				return True
		
		def contains_helper(obj, search):
			if isinstance(obj, dict):
				for key, value in obj.items():
					if search in key and isisntance_plus(value, search_type):
						yield True
					else:
						if isinstance(value, (dict, list)):
							for result in contains_helper(value, search):
								yield result

			elif isinstance(obj, list):
				for item in obj:
					for result in contains_helper(item, search):
						yield result
			
			
		return any(list(contains_helper(obj, search)))

class attribdict(defaultdict):
	'''	Default dictionary where keys can be accessed as attributes	'''
	def __init__(self, *args, **kwdargs):
		super(attribdict, self).__init__(attribdict, *args, **kwdargs)

	def __getattribute__(self, name):
		try:
			return object.__getattribute__(self, name)
		except AttributeError:
			try:
				return self[name]
			except KeyError:
				raise AttributeError(name)
		
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

	def __hash__(self):
		import copy
		
		def hash_helper(obj):
			if isinstance(obj, (set, tuple, list)):
				return tuple([hash_helper(element) for element in obj])    

			elif not isinstance(obj, dict):
				return hash(obj)

			new_obj = {}

			for key, value in obj.items():
				new_obj[key] = hash_helper(value)

			return hash(tuple(frozenset(sorted(new_obj.items()))))

		return hash_helper(self)

	def dir(self):
		tree_map = ['   .%s\t%s' %(key, type(value)) for key, value in self.items()]
		print('Attributes (Keys) map:\n%s' %('\n'.join(tree_map).expandtabs(30)))

	def factory(self, factory_type):
		self.default_factory = factory_type

	def lock(self):
		self.default_factory = None

	def extract(self, search):
		'''Pull all values of specified key (search)
		
		Attributes:
			search (Str): Search string

		Returns:
			generator
		'''
		return dictextractor.extract(self, search)
				
	def find(self, search, search_type=None):
		'''Pull all objects that contain keys of specified search.
		
		Attributes:
			search (Str): Search string
			search_type (type) : Value type
		Returns:
			generator
		'''
		return dictextractor.find(self, search, search_type)

	def where(self, search_value, search_key=None):
		'''Pull all objects that contain values of specified search.
		
		Attributes:
			search_value (Str): Search value
			search_key (Str) : Search for specific key that contains above value
		Returns:
			generator
		'''
		return dictextractor.where(self, search_value, search_key)

	def contains(self, search, search_type=None):
		'''Does the object contain ANY value or nested object with given name (search)
		
		Attributes:
			search (Str): Search string
			search_type (type) : Value type

		Returns:
			Bool
		'''
		return dictextractor.contains(self, search, search_type)
		