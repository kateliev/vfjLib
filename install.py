# encoding:	utf-8
# ----------------------------------------------------
# SCRIPT: 	Install
# DESC:		vfjLib installer
# ----------------------------------------------------
# (C) Vassil Kateliev, 2019  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies ------------------------------------
from __future__ import print_function
from distutils.sysconfig import get_python_lib
import os, sys

# - Init
moduleName = 'vfjLib'
moduleSubPath = 'Lib'

# - Functions --------------------------------------
def installModule(srcDir, modulePathName):
	sitePackDir = get_python_lib()
	fileName = os.path.join(sitePackDir, '%s.pth' %modulePathName)
	
	print('\nINFO:\tInstalling %s library...\nPATH:\t%r\nFILE:\t%r\n\n' %(moduleName, srcDir, fileName))

	file = open(fileName, 'w')
	file.write(srcDir)
	file.close()

	return fileName

# - Run -------------------------------------------
intallDir = os.path.join(os.path.dirname(os.path.normpath(os.path.abspath(sys.argv[0]))), moduleSubPath)
fileName = installModule(intallDir, moduleName)

print('DONE:\t%s installed!\nNOTE:\tRun script again if you change the location of the library' %moduleName)
