

import pathlib
print ("story 1 @:", pathlib.Path (__file__).parent.resolve ())


import soiree.instrument.clique as clique_intro
def start_clique ():
	group = clique_intro.start ()
	group ()