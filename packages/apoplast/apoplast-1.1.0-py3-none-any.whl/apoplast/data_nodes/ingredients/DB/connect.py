
'''
	import apoplast.data_nodes.ingredients.DB.connect as connect_to_ingredient
	ingredients_DB = connect_to_ingredient.DB (
		apoplast_variables = apoplast_variables
	)
'''

import pymongo

def DB (
	apoplast_variables = {}
):
	URL = apoplast_variables ["ingredients_DB"] ["URL"]
	DB_name = apoplast_variables ["ingredients_DB"] ["DB_name"]

	mongo_connection = pymongo.MongoClient (URL)
	DB = mongo_connection [ DB_name ]

	return DB