

'''
	
'''

'''
	itinerary:
'''
'''
{
    "name": "root",
    "type": "directory",
    "children": [
        {
            "name": "dir1",
            "type": "directory",
            "children": [
                {"name": "file1.txt", "type": "file"},
                {"name": "file2.txt", "type": "file"}
            ]
        },
        {
            "name": "dir2",
            "type": "directory",
            "children": [
                {"name": "file3.txt", "type": "file"}
            ]
        },
        {"name": "file4.txt", "type": "file"}
    ]
}
'''

import os
import json
from pathlib import Path

def thoroughly (scan_directory):

	original_scan_directory = str (scan_directory)

	def scan (directory):
		tree = {
			'name': os.path.basename (directory), 
			#'path': directory,
			'rel_path': str (Path (directory).relative_to (
				Path (original_scan_directory)
			)),
			'type': 'directory', 
			'children': []
		}

		# Iterate over the contents of the directory
		for item in os.listdir (directory):
			item_path = os.path.join (directory, item)

			# If the item is a subdirectory, recursively build its tree
			if os.path.isdir (item_path): 
				if os.path.islink (item_path):
					tree ['children'].append({
						'name': item, 
						#'path': item_path,
						'rel_path': str (Path (item_path).relative_to (
							Path (original_scan_directory)
						)),
						'type': "symlink directory"
					})
				else:
					tree ['children'].append (scan (item_path))
			else:
				if os.path.islink (item_path):
					the_type = "symlink"
				elif os.path.isfile (item_path):
					the_type = "file"
				else:
					the_type = "unknown"
			
				tree ['children'].append({
					'name': item, 
					#'path': item_path,
					'rel_path': str (Path (item_path).relative_to (
						Path (original_scan_directory)
					)),
					'type': the_type
				})

		return tree
	
	return scan (scan_directory)
	
	
def DFS (json_tree, callback):
	# Recursive case: If the node is a directory, recursively traverse its children
	if json_tree ['type'] == 'directory':
		processed_children = []
		
		assert ("children" in json_tree), json_tree
		
		for child in json_tree ['children']:
			DFS_proceeds = DFS (child, callback)
			processed_children.extend (DFS_proceeds)
			
		callback ({
			"rel_path": json_tree ["rel_path"],
			"type": json_tree ["type"]
		})
		
		# Include current directory in processed nodes
		return processed_children + [ json_tree ['name'] ] 
	
	else:
		callback ({
			"rel_path": json_tree ["rel_path"],
			"type": json_tree ["type"]
		})
		
		return []





