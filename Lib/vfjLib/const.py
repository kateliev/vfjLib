# ----------------------------------------------------
# MODULE: 	Constants | vfjLib
# ----------------------------------------------------
# (C) Vassil Kateliev, 2019  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# NOTE:		Module is kept Python 2 and 3 compatible!

# No warranties. By using this you agree
# that you use it at your own risk!


__version__ = "0.1.1"


# - VFJ Specific -------------------------------------
class cfg_vfj:
    def __init__(self):
        self.delimiter = "."
        self.delimiter_point = " "
        self.delimiter_node = self.delimiter_point * 2
        self.node_smooth = "s"
        self.node_close = "c"
        self.node_ttOffcurve = "o"
        self.node_g2 = "g2"

        self.vfj_version_value = 8  # Current VFJ version according to FL
        self.vfj_values_fileName = (
            "values"  # Special filename to hold all standalone values
        )

        self.major_split_suffix = "svfj"
        self.minor_split_suffix = "json"
        self.new_suffix = "new"
        self.glyph_split_suffix = self.minor_split_suffix
        self.feaure_split_suffix = self.minor_split_suffix
        self.master_split_suffix = self.minor_split_suffix


# - File Specific ------------------------------------
class cfg_filename:
    def __init__(self):
        # - List updated according to https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
        self.illegal = r"\' * + / : < > ? [ \ ] | \0".split(" ")
        self.illegal += [chr(i) for i in range(1, 32)]
        self.illegal += [chr(0x7F), " "]

        # - List updated according to https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
        self.reserved = "CLOCK$ A:-Z: CON PRN AUX NUL COM1 COM2 COM3 COM4 COM5 COM6 COM7 COM8 COM9 LPT1 LPT2 LPT3 LPT4 LPT5 LPT6 LPT7 LPT8 LPT9".lower().split(
            " "
        )

        # - Maximum file length
        self.max_len = 255

        # - Special character to fix filenames with
        self.special = "_"
        self.delimiter = "."
