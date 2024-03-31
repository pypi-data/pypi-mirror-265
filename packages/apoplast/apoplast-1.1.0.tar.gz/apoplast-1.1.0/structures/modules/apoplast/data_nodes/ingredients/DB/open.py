

'''
	mongod --dbpath ./../_mongo_data --port 39000
'''

'''
	import apoplast.data_nodes.ingredients.DB.open as ingredient_DB
	mongo_process = ingredient_DB.open (
		apoplast_variables = apoplast_variables
	)
	
	
	mongo_process.terminate ()

	#
	#	without this it might appear as if the process is still running.
	#
	import time
	time.sleep (2)
'''

import multiprocessing
import subprocess
import time
import os
import atexit

def open (
	apoplast_variables = {}
):
	port = apoplast_variables ["ingredients_DB"] ["port"]
	dbpath = apoplast_variables ["ingredients_DB"] ["path"]

	def open_process ():
		#script = f"mongod --dbpath '{ dbpath }' --port { port }"


		script = [
			"mongod", 

			'--dbpath', 
			#f"'{ dbpath }'", 
			f"{ dbpath }", 
			
			
			'--port', 
			str (port),
			
			'--bind_ip',
			'0.0.0.0'
		]

		# Start MongoDB as a subprocess
		the_process = subprocess.Popen (script)
		atexit.register (lambda: the_process.terminate ())

		time.sleep (5)
		
		return the_process

	os.makedirs (dbpath, exist_ok = True)

	mongo_process = open_process ()

	#mongo_process = multiprocessing.Process (target = open_process)
	#mongo_process.start ()

	return mongo_process;