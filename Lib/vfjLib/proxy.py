# encoding:	utf-8
# ----------------------------------------------------
# MODULE: 	Proxy | vfjLib
# ----------------------------------------------------
# (C) Vassil Kateliev, 2020  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# NOTE:		Module is kept Python 2 and 3 compatible!

# No warranties. By using this you agree
# that you use it at your own risk!

from __future__ import absolute_import, unicode_literals, print_function
from vfjLib.const import cfg_vfj

__version__ = '0.0.1'

# - Init ---------------------------------------------
current_config = cfg_vfj()

# -----------------------------------------------------
# - A collection of the simplest proxy objects possible
# -----------------------------------------------------
class jPoint(object):
	def __init__(self, x=None, y=None):
		self.x, self.y = x, y

	def __repr__(self):
		return self.string

	@property
	def tuple(self):
		return (self.x, self.y)

	@property
	def string(self):
		return '{0}{2}{1}'.format(self.x, self.y, current_config.delimiter_point)

	def dumps(self):
		return self.string

	@staticmethod
	def loads(string):
		xs, ys = string.split(current_config.delimiter_point)
		return jPoint(float(xs), float(ys))

class jNode(object):
	def __init__(self, x=None, y=None, nodeType=None, nodeSmooth=False, nodeName=None, nodeId=None):
		self.x, self.y = x, y
		self.type = nodeType
		self.smooth = nodeSmooth
		self.name = nodeName
		self.id = nodeId

	def __repr__(self):
		return self.string

	@property
	def tuple(self):
		return (self.x, self.y, self.type, self.smooth, self.name, self.id)

	@property
	def string(self):
		return '{0}{2}{1}'.format(self.x, self.y, current_config.delimiter_point) + ['', current_config.delimiter_point + current_config.node_smooth][self.smooth]

	def dumps(self):
		return self.string

	@staticmethod
	def loads(string):
		string_list = string.split(current_config.delimiter_point)
		node_smooth = True if len(string_list) == 3 and current_config.node_smooth in string_list else False
		return jNode(float(string_list[0]), float(string_list[1]), nodeType=None, nodeSmooth=node_smooth, nodeName=None, nodeId=None)

			


# -- Test --------------------------------------
if __name__ == '__main__':
	jp = jNode(10,10)
	ja = jNode.loads('20 20 s')
	print(ja.smooth)