
'''
	import soiree.stage.layer.start_dev as flask_dev
'''

import soiree.stage.layer as stage_flask

def start (port):
	print ('starting')
	
	app = stage_flask.build ()
	app.run (port = port)

	return;
	
#if __name__ == "__main__":
#	start ()