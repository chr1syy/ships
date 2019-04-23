import json

def get_ships(id):

	ships = {}

	with open('/home/ubuntu/eos/phobos/invtypes.json') as f:
		d = json.load(f)
		for x in d:
			if d[x]['groupID'] == id:
				if d[x]['published']:
					ships.update( { d[x]['typeName'] : d[x]['typeID'] } )


	return ships
#example print

#for (key,value) in frig.items():
#	print(str(key)+"::"+str(value))
#print('\n\n')
#for (key,value) in des.items():
#        print(str(key)+"::"+str(value))

