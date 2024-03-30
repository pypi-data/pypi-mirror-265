





'''
	python3 status.py "paths/directory/scan_tree/_status/1/status_1.py"
'''

import ships.paths.directory.scan_tree as scan_tree
import json
import rich

def rel_path (directory):
	import pathlib
	this_directory = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	import sys
	return normpath (join (this_directory, directory))

def check_1 ():
	cryo = rel_path ("cryo")
	
	the_tree_scan = scan_tree.thoroughly (
		cryo
	)
	rich.print_json (data = the_tree_scan)
	
	assert (
		the_tree_scan == {
		  "name": "cryo",
		  "rel_path": ".",
		  "type": "directory",
		  "children": [
			{
			  "name": "3",
			  "rel_path": "3",
			  "type": "directory",
			  "children": [
				{
				  "name": "3.txt",
				  "rel_path": "3/3.txt",
				  "type": "file"
				},
				{
				  "name": "9",
				  "rel_path": "3/9",
				  "type": "directory",
				  "children": [
					{
					  "name": "9.txt",
					  "rel_path": "3/9/9.txt",
					  "type": "file"
					}
				  ]
				}
			  ]
			},
			{
			  "name": "symlink_to_1",
			  "rel_path": "symlink_to_1",
			  "type": "symlink directory"
			},
			{
			  "name": "symlink_to_1.txt",
			  "rel_path": "symlink_to_1.txt",
			  "type": "symlink"
			},
			{
			  "name": "1.txt",
			  "rel_path": "1.txt",
			  "type": "file"
			},
			{
			  "name": "2",
			  "rel_path": "2",
			  "type": "directory",
			  "children": [
				{
				  "name": "2.txt",
				  "rel_path": "2/2.txt",
				  "type": "file"
				},
				{
				  "name": "55",
				  "rel_path": "2/55",
				  "type": "directory",
				  "children": [
					{
					  "name": "55.txt",
					  "rel_path": "2/55/55.txt",
					  "type": "file"
					}
				  ]
				}
			  ]
			},
			{
			  "name": "1",
			  "rel_path": "1",
			  "type": "directory",
			  "children": [
				{
				  "name": "1.py",
				  "rel_path": "1/1.py",
				  "type": "file"
				}
			  ]
			}
		  ]
		}
	), the_tree_scan
	
	places = []
	def place_found (place):
		#rich.print_json (data = place)
		places.append (place)

	scan_tree.DFS (the_tree_scan, place_found)

	rich.print_json (data = places)

	assert (
		places ==
		[
		  {
			"rel_path": "3/3.txt",
			"type": "file"
		  },
		  {
			"rel_path": "3/9/9.txt",
			"type": "file"
		  },
		  {
			"rel_path": "3/9",
			"type": "directory"
		  },
		  {
			"rel_path": "3",
			"type": "directory"
		  },
		  {
			"rel_path": "symlink_to_1",
			"type": "symlink directory"
		  },
		  {
			"rel_path": "symlink_to_1.txt",
			"type": "symlink"
		  },
		  {
			"rel_path": "1.txt",
			"type": "file"
		  },
		  {
			"rel_path": "2/2.txt",
			"type": "file"
		  },
		  {
			"rel_path": "2/55/55.txt",
			"type": "file"
		  },
		  {
			"rel_path": "2/55",
			"type": "directory"
		  },
		  {
			"rel_path": "2",
			"type": "directory"
		  },
		  {
			"rel_path": "1/1.py",
			"type": "file"
		  },
		  {
			"rel_path": "1",
			"type": "directory"
		  },
		  {
			"rel_path": ".",
			"type": "directory"
		  }
		]
	)	
		
checks = {
	"check 1": check_1
}