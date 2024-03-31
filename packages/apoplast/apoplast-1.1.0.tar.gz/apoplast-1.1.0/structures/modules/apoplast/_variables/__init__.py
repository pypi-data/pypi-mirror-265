

'''
	from apoplast._variables import prepare_variables
	apoplast_variables = prepare_variables ({
		"ingredients_DB": {
			"name": "apoplast ingredients",
			"port": "39001"
		}
	})
'''

import pathlib
from os.path import dirname, join, normpath
import sys

import pydash

def prepare_variables (
	variables = {}
):
	this_folder = pathlib.Path (__file__).parent.resolve ()	

	return pydash.merge (
		{
			"ingredients_DB": {
				"URL": "mongodb://localhost:39000/",
				"port": "39000",
				"DB_name": "ingredients",
				"path": str (normpath (join (this_folder, "../data_nodes/ingredients/_mongo_data")))
			}
		},
		variables
	)