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


import copy
import json
import json.scanner
import os
import shutil
from collections import OrderedDict

from vfjLib.const import cfg_vfj
from vfjLib.object import attribdict, dictextractor
from vfjLib.parser import string2filename, vfj_decoder, vfj_encoder
from vfjLib.proxy import jGlyph

__version__ = "0.3.1"


# - Objects -----------------------------------------
class vfjFont(attribdict):
    def __init__(self, vfj_path=None):
        self.vfj_path = vfj_path
        if self.vfj_path is not None:
            self._vfj_read(self.vfj_path)

        self.__glyphs_cache = []

    def __repr__(self):
        if len(self.keys()):
            return "<{} name={}, masters={}, glyphs={}, version={}>".format(
                self.__class__.__name__,
                self.font.info.tfn,
                len(self.font.masters),
                self.font.glyphsCount,
                self.font.info.version,
            )
        else:
            return (
                "<%s name=None, masters=None, glyphs=None, version=None>"
                % self.__class__.__name__
            )

    # - Internals --------------------------------------------------
    def _vfj_read(self, vfj_path):
        self.vfj_path = vfj_path
        self.update(json.load(open(vfj_path), cls=vfj_decoder))

    def _vfj_write(self, vfj_path, overwrite=True):
        if os.path.exists(vfj_path):
            if not overwrite:
                counter = 0
                prefix, ext = os.path.splitext(vfj_path)

                # - Handle clash - give unique filename
                while os.path.isfile(vfj_path):
                    counter += 1
                    vfj_path = f"{prefix}.{counter}{ext}"

        json.dump(self, open(vfj_path, "w"), cls=vfj_encoder, sort_keys=True, indent=4)

    def _vfj_split(self, split_path, overwrite=False):
        """Splits a single VFJ file into Split VFJ Format (folder)."""

        # - Init
        cfg_file = cfg_vfj()
        split = self.font

        # - Create path
        if os.path.isfile(split_path):
            root = os.path.splitext(split_path)[0]
        else:
            root = os.path.join(split_path, string2filename(self.font.info.tfn))

        # - Handle existing write path
        test_root = f"{root}.{cfg_file.major_split_suffix}"

        if os.path.exists(test_root):
            if overwrite:
                shutil.rmtree(test_root)
            else:
                counter = 0

                # - Handle clash - give unique folder name
                while os.path.exists(test_root):
                    counter += 1
                    test_root = "{}.{}.{}".format(
                        root,
                        counter,
                        cfg_file.major_split_suffix,
                    )

        root = test_root
        os.mkdir(root)

        # - Setup aggregation dict to contain all loose values
        agg = attribdict()

        # - Process split
        for key, value in split.items():
            if isinstance(value, dict):
                item_name = f"{key}.{cfg_file.minor_split_suffix}"
                json.dump(
                    value,
                    open(os.path.join(root, item_name), "w"),
                    cls=vfj_encoder,
                    sort_keys=True,
                    indent=4,
                )

            elif isinstance(value, list):
                subfolder = os.path.join(root, key)
                os.mkdir(subfolder)

                for item_index in range(len(value)):
                    item_name = string2filename(
                        f"{key}.{item_index}", cfg_file.feaure_split_suffix
                    )

                    if value[item_index].has_key("name") and not value[
                        item_index
                    ].has_key("tsn"):
                        item_name = string2filename(
                            value[item_index].name, cfg_file.glyph_split_suffix, True
                        )

                    elif value[item_index].has_key("name"):
                        item_name = string2filename(
                            value[item_index].name, cfg_file.glyph_split_suffix
                        )

                    elif value[item_index].has_key("tfn"):
                        item_name = string2filename(
                            value[item_index].tfn, cfg_file.master_split_suffix
                        )

                    elif value[item_index].has_key("fontMaster"):
                        item_name = string2filename(
                            value[item_index].fontMaster.name,
                            cfg_file.master_split_suffix,
                        )

                    json.dump(
                        value[item_index],
                        open(os.path.join(subfolder, item_name), "w"),
                        cls=vfj_encoder,
                        sort_keys=True,
                        indent=4,
                    )
            else:
                agg[key] = value

        json.dump(
            agg,
            open(
                os.path.join(
                    root,
                    string2filename(
                        cfg_file.vfj_values_fileName, cfg_file.minor_split_suffix
                    ),
                ),
                "w",
            ),
            cls=vfj_encoder,
            sort_keys=True,
            indent=4,
        )

    def _vfj_merge(self, merge_path):
        """Merges a Split VFJ Format (folder) into single VFJ file."""

        from vfjLib.object import attribdict

        cfg_file = cfg_vfj()
        root = merge_path
        self["version"] = cfg_file.vfj_version_value
        self["font"] = attribdict()

        for dirName, subdirList, fileList in os.walk(root, topdown=True):
            if dirName == root:
                for key in subdirList:
                    self.font[key] = []

                for fileName in fileList:
                    if fileName == "{}.{}".format(
                        cfg_file.vfj_values_fileName,
                        cfg_file.minor_split_suffix,
                    ):
                        self.font.update(
                            json.load(
                                open(os.path.join(dirName, fileName)), cls=vfj_decoder
                            )
                        )
                    else:
                        self.font[fileName.split(".")[0]] = json.load(
                            open(os.path.join(dirName, fileName)), cls=vfj_decoder
                        )

            else:
                if os.path.split(dirName)[1] in self.font.keys():
                    for fileName in fileList:
                        self.font[os.path.split(dirName)[1]].append(
                            json.load(
                                open(os.path.join(dirName, fileName)), cls=vfj_decoder
                            )
                        )

        self._vfj_rebuild_glyph_array()
        self.font.lock()

    def _vfj_rebuild_glyph_array(self):
        """Reorders glyphs so that the base glyphs are first and glyphs that are references are last."""

        glyph_base, glyph_ref, glyph_comp, glyph_other = [], [], [], []

        for glyph in self.font.glyphs:
            if glyph.contains("elementData", unicode):
                glyph_ref.append(glyph)

            elif glyph.contains("component"):
                glyph_comp.append(glyph)

            elif glyph.contains("elementData", dict):
                if glyph not in glyph_ref and glyph not in glyph_comp:
                    glyph_base.append(glyph)
            else:
                glyph_other.append(glyph)

        self.font.glyphs = glyph_base + glyph_ref + glyph_comp + glyph_other
        self.font.glyphsCount = len(self.font.glyphs)

    def _vfj_split_glyphs_master(self):
        """Splits glyphs by master."""
        masters = self.getMasterNames()
        glyph_layer_dict = {master_name: [] for master_name in masters}

        # - Split glyphs by layers
        if hasattr(self.font, "glyphs") and len(self.font.glyphs):
            for glyph in self.font.glyphs:
                if hasattr(glyph, "layers") and len(glyph.layers):
                    for master_name in masters:
                        layer_search = list(
                            dictextractor.where(glyph.layers, master_name, "name")
                        )
                        if len(layer_search):
                            new_glyph = attribdict(glyph)
                            new_glyph.layers = layer_search
                            glyph_layer_dict[master_name].append(new_glyph)

        return glyph_layer_dict

    def _vfj_split_font_master(self):
        """Split font into multiple single master fonts."""
        font_layer_list = []
        masters = self.getMasterNames()
        glyph_layer_dict = self._vfj_split_glyphs_master()

        if hasattr(self.font, "masters") and len(self.font.masters):
            # - Split everything else
            for master_name in masters:
                new_font = copy.deepcopy(self)
                new_font.lock()

                new_font.font.pop("axes", None)
                new_font.font.pop("instaces", None)

                new_font.font.defaultMaster = master_name
                new_font.font.masters = [
                    attribdict(
                        {
                            "fontMaster": list(
                                dictextractor.where(
                                    self.font.masters, master_name, "name"
                                )
                            )[0]
                        }
                    )
                ]
                new_font.font.glyphs = glyph_layer_dict[master_name]

                font_layer_list.append(new_font)

            return font_layer_list

    # - Externals --------------------------------------------------
    # -- I/O -------------------------------------------------------
    def save(self, vfj_path=None, split=False, overwrite=False):
        if vfj_path is None:
            vfj_path = self.vfj_path

        if not split:
            self._vfj_write(vfj_path, overwrite)
        else:
            self._vfj_split(vfj_path, overwrite)

    def open(self, vfj_path=None, merge=False):
        if not merge:
            self._vfj_read(vfj_path)
        else:
            self._vfj_merge(vfj_path)

    # - Layers -----------------------------------------------------
    def getMasterNames(self):
        return [item.name for item in self.extract("fontMaster")]

    # - Glyphs -----------------------------------------------------
    def getGlyphSet(self, layer_name=None, use_cache=True, extend=None):
        # - Init
        layer_name = self.font.defaultMaster if layer_name is None else layer_name
        glyphs_dict = OrderedDict()

        # - Process
        if hasattr(self.font, "glyphs") and len(self.font.glyphs):
            if not use_cache or not len(self.__glyphs_cache):
                self.__glyphs_cache = self._vfj_split_glyphs_master()

            layer_glyphs = self.__glyphs_cache[layer_name]

            for glyph in layer_glyphs:
                glyphs_dict[glyph.name] = glyph if extend is None else extend(glyph)

        return glyphs_dict

    def getCharacterMapping(self, layer_name=None):
        # - Init
        unicodes_dict = OrderedDict()
        layer_name = self.font.defaultMaster if layer_name is None else layer_name

        # - Process
        if hasattr(self.font, "glyphs") and len(self.font.glyphs):
            for glyph in self.font.glyphs:
                if hasattr(glyph, "unicode") and len(glyph.unicode):
                    unicodes_dict.setdefault(glyph.unicode, []).append(glyph.name)

        return unicodes_dict
