# encoding:	utf-8
# ----------------------------------------------------
# SCRIPT: vfj2single
# DESC: A tool for splinting multiple master VFJ into 
# DESC: single master font files.
# ----------------------------------------------------
# (C) Vassil Kateliev, 2020  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# No warranties. By using this you agree
# that you use it at your own risk!

from __future__ import absolute_import, print_function, unicode_literals
import os, sys
import vfjLib

__version__ = '0.0.2'

# - String --------------------------------
help_str='''VFJ2SINGLE:  A tool for splinting multiple master VFJ into single master font files.
Usage:
	vfj2git --merge <filenames (VFJ)> : Merge multiple VFJ single master files into one multiple master file.
	vfj2git --split <filename (VFJ)> : Split a multiple master VFJ font file.
'''
# - Init ----------------------------------
basePath = os.getcwd()
run_args = sys.argv[1:]

# - RUN ----------------------------------
'''
if '--merge' in run_args:
	file_name = run_args[run_args.index('--merge') + 1]
	new_font = vfjLib.vfjFont()
	new_font.open(file_name, merge=True)
	new_font.save('%s.%s' %(file_name.split('.')[0],'vfj'))
	print('\nVFJ2SINGLE:\tDone merging %s.' %file_name)
'''

if '--split' in run_args:
	arg_name = run_args[run_args.index('--split') + 1]
	file_path, file_name = os.path.split(arg_name)

	old_font = vfjLib.vfjFont(arg_name)
	font_list = old_font._vfj_split_font_master()
	
	for new_font in font_list:
		new_suffix = new_font.font.masters[0].fontMaster.name
		new_filename = '.'.join([file_name.split('.')[0], new_suffix, 'vfj'])
		save_path = os.path.join(file_path, new_filename)
		new_font._vfj_write(save_path, True)
		print('WRITE:\t {};'.format(save_path))

	print('\nVFJ2SINGLE:\tDone splitting %s.' %file_name)

if '--help' in run_args:
	print(help_str)
	print(__version__)
	
