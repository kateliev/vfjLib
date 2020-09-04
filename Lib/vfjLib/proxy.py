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
from vfjLib.object import attribdict
from vfjLib.const import cfg_vfj

__version__ = '0.0.1'

# - Init ---------------------------------------------
current_config = cfg_vfj()


# - Simplest objects possible ------------------------
class jPoint(object):
	'''jPoint'''
	def __init__(self, x=None, y=None, transform=None):
		self.x, self.y = x, y
		self.transform = transform

	def __repr__(self):
		return '<{} x={0}, y={1}, transform={2}>'.format(self.__class__.__name__, self.x, self.y, self.transform)

	@property
	def tuple(self):
		return (self.x, self.y)

	@property
	def string(self):
		x = int(self.x) if self.x.is_integer() else self.x
		y = int(self.y) if self.y.is_integer() else self.y
		return '{0}{2}{1}'.format(x, y, current_config.delimiter_point)

	def dumps(self):
		return self.string

	@staticmethod
	def loads(string):
		xs, ys = string.split(current_config.delimiter_point)
		return jPoint(float(xs), float(ys))

class jNode(object):
	'''jNode'''
	def __init__(self, x=None, y=None, nodeType=None, nodeSmooth=False, nodeG2=False, nodeName=None, nodeId=None, transform=None):
		self.x, self.y = x, y
		self.id = nodeId
		self.g2 = nodeG2
		self.name = nodeName
		self.type = nodeType
		self.smooth = nodeSmooth
		self.transform = transform

	def __repr__(self):
		return '<{} x={}, y={}, type={}, smooth={}, g2={}, name={}, id={}, transform={}>'.format(self.__class__.__name__, self.x, self.y, self.type, self.smooth, self.g2, self.name, self.id, self.transform)

	@property
	def tuple(self):
		return (self.x, self.y, self.type, self.smooth, self.name, self.id)

	@property
	def string(self):
		node_config = []
		x = int(self.x) if self.x.is_integer() else self.x
		y = int(self.y) if self.y.is_integer() else self.y
		
		node_config.append(str(x))
		node_config.append(str(y))

		if self.smooth: node_config.append(current_config.node_smooth)
		#if self.type == 'offcurve': node_config.append(current_config.node_ttOffcurve)
		if self.g2: node_config.append(current_config.node_g2)

		return current_config.delimiter_point.join(node_config)

	def dumps(self):
		return self.string

	@staticmethod
	def loads(string):
		string_list = string.split(current_config.delimiter_point)
		node_smooth = True if len(string_list) >= 3 and current_config.node_smooth in string_list else False
		node_type = 'offcurve' if len(string_list) >= 3 and current_config.node_ttOffcurve in string_list else None
		node_g2 = True if len(string_list) >= 3 and current_config.node_g2 in string_list else False

		return jNode(float(string_list[0]), float(string_list[1]), nodeType=node_type, nodeSmooth=node_smooth, nodeG2=node_g2, nodeName=None, nodeId=None)

class jContour(object):
	'''jContour'''
	def __init__(self, jNodeList=[], isOpen=False, contourId=None, transform=None):
		self.nodes = jNodeList
		self.open = isOpen
		self.id = contourId
		self.transform = transform

	def __repr__(self):
		return '<{} nodes={}, open={}, transform={}>'.format(self.__class__.__name__, len(self.nodes), self.open, self.transform)

	@property
	def tuple(self):
		return ([node.tuple for node in self.nodes], self.open, self.id, self.transform)

	@property
	def string(self):
		string_nodes = []
		node_accumulator = []

		for node in self.nodes:
			if node.type == 'offcurve': 
				node_accumulator.append(node.string)

			elif node.type == 'curve' or node.type == 'qcurve':
				node_accumulator.append(node.string)
				string_nodes.append(current_config.delimiter_node.join(node_accumulator))
				node_accumulator = []

			elif node.type == 'line':
				string_nodes.append(node.string)

		return string_nodes

	def dumps(self):
		return self.string

	@staticmethod
	def loads(stringList, isOpen=False, transform=None):
		contour_open = isOpen
		contour_nodes = []
		
		node_first = True
		node_seen = None

		for node_string in stringList:
			temp_nodes = node_string.split(current_config.delimiter_node)

			if len(temp_nodes) == 1:
				new_node = jNode.loads(temp_nodes[0])
				
				if node_first:
					if contour_open: 
						new_node.type = 'move'
					else:
						new_node.type = 'line'

					node_first = False
				
				if node_seen is not None:
					new_node.type = 'line'

				node_seen = new_node
				contour_nodes.append(new_node)


			if len(temp_nodes) > 1:
				temp_jnodes = [jNode.loads(node) for node in node_string.split(current_config.delimiter_node)]

				for new_node in temp_jnodes[:-1]:
					new_node.type = 'offcurve'
					node_seen = new_node
					contour_nodes.append(new_node)

				temp_jnodes[-1].type = 'qcurve' if node_seen.type is 'offcurve' and node_seen.smooth else 'curve'

				node_seen = temp_jnodes[-1]
				contour_nodes.append(temp_jnodes[-1])

		return jContour(contour_nodes, contour_open, transform)
			
# - Container objects -------------------------------------------
class jElement(attribdict):
	'''jElement'''
	def __init__(self, data):
		super(jElement, self).__init__(data)
		self.lock()

		if hasattr(self, 'contours'):
			new_contours_container = []
			
			for contour in self.contours:
				contour.lock()
				contour_nodes = contour.nodes
				contour_open = contour.open if hasattr(contour, 'open') else False
				
				contour_transform = contour.transform if hasattr(contour, 'transform') else None
				new_contours_container.append(jContour.loads(contour_nodes, contour_open, contour_transform))

			self.contours = new_contours_container
	
	def __repr__(self):
		return '<{}: contours={}, transform={}>'.format(self.__class__.__name__, len(self.contours), self.transform if hasattr(self, 'transform') else None)

class jLayer(attribdict):
	'''jLayer'''
	def __init__(self, data):
		super(jLayer, self).__init__(data)
		self.lock()

		if hasattr(self, 'elements'):
			new_elements_container = []
			
			for element in self.elements:
				element.lock()
				new_element = jElement(element.elementData)
				if hasattr(element, 'transform'): new_element.transform = element.transform
				new_elements_container.append(new_element)

			self.elements = new_elements_container

	def __repr__(self):
		return '<{}: elements={}, transform={}>'.format(self.__class__.__name__, len(self.elements), self.transform if hasattr(self, 'transform') else None)


# -- Test --------------------------------------
if __name__ == '__main__':
	from vfjLib import vfjFont
	vf = vfjFont(r'd:\Achates-3Wd.vfj')
	gs = vf.getGlyphSet()
	ll = gs['O'].layers[0]
	#print(ll.elements[0].elementData.contours)
	print(jLayer(ll))
	