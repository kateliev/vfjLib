# ----------------------------------------------------
# MODULE: 	Proxy | vfjLib
# ----------------------------------------------------
# (C) Vassil Kateliev, 2020  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# NOTE:		Module is kept Python 2 and 3 compatible!

# No warranties. By using this you agree
# that you use it at your own risk!

from vfjLib.const import cfg_vfj
from vfjLib.object import attribdict

__version__ = "0.1.5"

# - Init ---------------------------------------------
current_config = cfg_vfj()


# - Simplest objects possible ------------------------
class jPoint:
    """jPoint"""

    def __init__(self, x=None, y=None, transform=None):
        self.x, self.y = x, y
        self.transform = transform

    def __repr__(self):
        return f"<{self.__class__.__name__} x={self.__class__.__name__}, y={self.x}, transform={self.y}>"

    @property
    def tuple(self):
        return (self.x, self.y)

    @property
    def string(self):
        x = int(self.x) if self.x.is_integer() else self.x
        y = int(self.y) if self.y.is_integer() else self.y
        return f"{x}{current_config.delimiter_point}{y}"

    def dumps(self):
        return self.string

    @staticmethod
    def loads(string):
        xs, ys = string.split(current_config.delimiter_point)
        return jPoint(float(xs), float(ys))


class jNode:
    """jNode"""

    def __init__(
        self,
        x=None,
        y=None,
        node_type=None,
        node_smooth=False,
        node_g2=False,
        node_name=None,
        node_id=None,
        transform=None,
    ):
        self.x, self.y = x, y
        self.id = node_id
        self.g2 = node_g2
        self.name = node_name
        self.type = node_type
        self.smooth = node_smooth
        self.transform = transform

    def __repr__(self):
        return f"<{self.__class__.__name__} x={self.x}, y={self.y}, type={self.type}, smooth={self.smooth}, g2={self.g2}, name={self.name}, id={self.id}, transform={self.transform}>"

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

        if self.smooth:
            node_config.append(current_config.node_smooth)
        # if self.type == 'offcurve': node_config.append(current_config.node_ttOffcurve)
        if self.g2:
            node_config.append(current_config.node_g2)

        return current_config.delimiter_point.join(node_config)

    def dumps(self):
        return self.string

    @staticmethod
    def loads(string):
        string_list = string.split(current_config.delimiter_point)
        node_smooth = (
            True
            if len(string_list) >= 3 and current_config.node_smooth in string_list
            else False
        )
        node_type = (
            "offcurve"
            if len(string_list) >= 3 and current_config.node_ttOffcurve in string_list
            else None
        )
        node_g2 = (
            True
            if len(string_list) >= 3 and current_config.node_g2 in string_list
            else False
        )

        return jNode(
            float(string_list[0]),
            float(string_list[1]),
            node_type=node_type,
            node_smooth=node_smooth,
            node_g2=node_g2,
            node_name=None,
            node_id=None,
        )


class jContour:
    """jContour"""

    def __init__(self, jNodeList=[], is_open=False, contour_id=None, transform=None):
        self.nodes = jNodeList
        self.open = is_open
        self.id = contour_id
        self.transform = transform

    def __repr__(self):
        return f"<{self.__class__.__name__} nodes={len(self.nodes)}, open={self.open}, transform={self.transform}>"

    @property
    def tuple(self):
        return ([node.tuple for node in self.nodes], self.open, self.id, self.transform)

    @property
    def string(self):
        string_nodes = []
        node_accumulator = []

        for node in self.nodes:
            if node.type == "offcurve":
                node_accumulator.append(node.string)

            elif node.type == "curve" or node.type == "qcurve":
                node_accumulator.append(node.string)
                string_nodes.append(
                    current_config.delimiter_node.join(node_accumulator)
                )
                node_accumulator = []

            elif node.type == "line":
                string_nodes.append(node.string)

        return string_nodes

    def dumps(self):
        return self.string

    @staticmethod
    def loads(stringList, is_open=False, transform=None):
        contour_open = is_open
        contour_nodes = []

        node_first = True
        node_seen = None

        for node_string in stringList:
            temp_nodes = node_string.split(current_config.delimiter_node)

            if len(temp_nodes) == 1:
                new_node = jNode.loads(temp_nodes[0])

                if node_first:
                    if contour_open:
                        new_node.type = "move"
                    else:
                        new_node.type = "line"

                    node_first = False

                if node_seen is not None:
                    new_node.type = "line"

                node_seen = new_node
                contour_nodes.append(new_node)

            if len(temp_nodes) > 1:
                temp_jnodes = [
                    jNode.loads(node)
                    for node in node_string.split(current_config.delimiter_node)
                ]

                for new_node in temp_jnodes[:-1]:
                    new_node.type = "offcurve"
                    node_seen = new_node
                    contour_nodes.append(new_node)

                temp_jnodes[-1].type = (
                    "qcurve"
                    if node_seen.type == "offcurve" and node_seen.smooth
                    else "curve"
                )

                node_seen = temp_jnodes[-1]
                contour_nodes.append(temp_jnodes[-1])

        return jContour(contour_nodes, contour_open, transform)


# - Container objects -------------------------------------------
class jElement(attribdict):
    """jElement"""

    def __init__(self, data):
        super().__init__(data)
        self.lock()

        if hasattr(self, "contours"):
            new_contours_container = []

            for contour in self.contours:
                contour.lock()
                contour_nodes = contour.nodes
                contour_open = contour.open if hasattr(contour, "open") else False
                contour_transform = (
                    dict(contour.transform.items())
                    if hasattr(contour, "transform")
                    else None
                )
                new_element = jContour.loads(
                    contour_nodes, contour_open, contour_transform
                )
                new_contours_container.append(new_element)

            self.contours = new_contours_container

    def __repr__(self):
        return "<{}: contours={}, transform={}>".format(
            self.__class__.__name__,
            len(self.contours),
            self.transform if hasattr(self, "transform") else None,
        )


class jComponent(attribdict):
    """jComponent"""

    def __init__(self, data):
        super().__init__(data)
        self.lock()
        self.base = self.glyphName

    def __repr__(self):
        return "<{}: name={}, transform={}>".format(
            self.__class__.__name__,
            self.glyphName,
            self.transform if hasattr(self, "transform") else None,
        )


class jLayer(attribdict):
    """jLayer"""

    def __init__(self, data):
        super().__init__(data)
        self.lock()

        if hasattr(self, "elements") and len(self.elements):
            new_elements_container = []

            for element in self.elements:
                element.lock()

                if hasattr(element, "elementData") and len(element.elementData):
                    element.elementData.pop("locked", None)
                    new_element = jElement(element.elementData)
                    if hasattr(element, "transform"):
                        new_element.transform = dict(element.transform.items())
                    new_elements_container.append(new_element)

                if hasattr(element, "component"):
                    element.component.pop("locked", None)
                    new_element = jComponent(element.component)
                    if hasattr(element, "transform"):
                        new_element.transform = dict(element.transform.items())
                    new_elements_container.append(new_element)

            self.elements = new_elements_container

    def __repr__(self):
        return f"<{self.__class__.__name__}: name={self.name}, elements={len(self.elements)}>"


class jGlyph(attribdict):
    """jGlyph"""

    def __init__(self, data):
        super().__init__(data)
        self.lock()

        if hasattr(self, "layers") and len(self.layers):
            new_layers_container = []

            for layer in self.layers:
                layer.lock()
                new_layer = jLayer(layer)
                new_layers_container.append(new_layer)

            self.layers = new_layers_container

    def __repr__(self):
        return f"<{self.__class__.__name__}: name={self.name}, unicode={self.unicode}, layers={len(self.layers)}>"


# -- Test --------------------------------------
if __name__ == "__main__":
    from vfjLib import vfjFont

    # vf = vfjFont(r'd:\Achates-3Wd.vfj')
    vf = vfjFont(r"d:\dida.vfj")
    # gs = vf.getGlyphSet(extend=jGlyph)
    gs = vf.getGlyphSet()
    print(gs["Q"].layers[0].dir())
    # ll = gs['Odieresis'].layers[0]
    # jg = jGlyph(gs['Odieresis'])
    # print(ll.elements[0].elementData.contours)
    # print(jLayer(ll).anchors[0].dir())
    # print(jg.layers[0].elements[1].contours[0].nodes[0])
