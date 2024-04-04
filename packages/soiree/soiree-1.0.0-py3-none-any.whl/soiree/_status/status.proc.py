




def add_paths_to_system (paths):
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_folder = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_folder, path)))

add_paths_to_system ([
	'../../../modules',
	'../../../modules_pip'
])


import soiree._status as soiree_status
soiree_status.start ()
