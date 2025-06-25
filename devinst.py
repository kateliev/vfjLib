# SCR : vfjLib Dinamic Dev Installer
# VER : 0.02

import os
import sys
# - Dependencies --------------------------
from distutils.sysconfig import get_python_lib

# - Init
moduleName = "vfjLib"
moduleSubPath = "Lib"


# - Functions --------------------------
def installModule(srcDir, modulePathName):
    sitePackDir = get_python_lib()
    fileName = os.path.join(sitePackDir, "%s.pth" % modulePathName)

    print(
        "\nINFO:\t Installing %s library...\nPATH:\t%r\nFILE:\t%r\n\n"
        % (moduleName, srcDir, fileName)
    )

    file = open(fileName, "w")
    file.write(srcDir)
    file.close()

    return fileName


# - Run --------------------------
intallDir = os.path.join(
    os.path.dirname(os.path.normpath(os.path.abspath(sys.argv[0]))), moduleSubPath
)
fileName = installModule(intallDir, moduleName)

print(
    "DONE:\t%s installed!\nNOTE:\tRun script again if you change the location of the library"
    % moduleName
)
