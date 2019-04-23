from django.shortcuts import render
from django.http import HttpResponse
from . import get_ships
from eos import *
from eos.item_filter import *
import json
# Create your views here.

def index(request):
	response = HttpResponse()
	with open('/home/ubuntu/eos/phobos/invgroups.json') as f:
		d = json.load(f)
		for x in d:
			if d[x]['categoryID'] == 6:
				response.write("<a href='list/"+str(d[x]['groupID'])+"'>"+d[x]['groupName']+"</a><br>")
	return response

def list(request, categoryid):
        ships = get_ships.get_ships(categoryid)
        response = HttpResponse()
        for (key,value) in ships.items():
                response.write("<a href='/ships/"+str(value)+"'>"+str(key)+"</a><br>")
        return response

def detail(request, shipid):
	fit = ""
	data_handler = JsonDataHandler('/home/ubuntu/eos/phobos/')  # Folder with Phobos data dump
	cache_handler = JsonCacheHandler('/home/ubuntu/eos/cache/eos_tq.json.bz2')
	SourceManager.add('tiamat', data_handler, cache_handler, make_default=True)

	skill_groups = set(row['groupID'] for row in data_handler.get_evegroups() if row['categoryID'] == 16)
	skills = set(row['typeID'] for row in data_handler.get_evetypes() if row['groupID'] in skill_groups)

	fit = Fit()
	fit.ship = Ship(shipid)

	for skill_id in skills:
		fit.skills.add(Skill(skill_id, level=5))

	fit.validate()

	response = HttpResponse()
#	with open('/home/ubuntu/eos/phobos/invtypes.json') as f:
#		d = json.load(f)
#		ship_name = d[shipid]['typeName']
#
#	response.write(ship_name)
	response.write("<br>")
	response.write("mass: "+str(fit.ship.attrs[4]))
	response.write("<br>")
	response.write("powergrid output: "+str(fit.ship.attrs[11]))
	response.write("<br>")
	response.write("cpu output: "+str(fit.ship.attrs[48]))
	response.write("<br>")
	response.write("velocity: "+str(fit.ship.attrs[37]))
	response.write("<br>")
	response.write("signature: "+str(fit.ship.attrs[552]))
	response.write("<br>")
	response.write("scan res: "+str(fit.ship.attrs[564]))
	response.write("<br>")
	response.write("targeting range: "+str(fit.ship.attrs[76]))
	response.write("<br>")
	response.write("cap capacity: "+str(fit.ship.attrs[79])+" <- this cant be")
	response.write("<br>")
	response.write("warp speed: "+str(fit.ship.attrs[600]))
	response.write("<br>")
	response.write("cargo capacity: "+str(fit.ship.attrs[38]))
	response.write("<br>")
	response.write("drone cargo capacity: "+str(fit.ship.attrs[283])+"<br>")
	response.write("drone bandwidth: "+str(fit.ship.attrs[1271])+"<br>")
	response.write("high slots: "+str(fit.ship.attrs[14])+"<br>")
	response.write("med slots: "+str(fit.ship.attrs[13])+"<br>")
	response.write("low slots: "+str(fit.ship.attrs[12])+"<br>")
	response.write("rig slots: "+str(fit.ship.attrs[1137])+"<br>")
	response.write("armor hp: "+str(fit.ship.attrs[265])+"<br>")
	response.write("hp: "+str(fit.ship.attrs[9])+"<br>")
	response.write("shield capacity: "+str(fit.ship.attrs[263])+"<br>")
	response.write("agility: "+str(fit.ship.attrs[70])+"<br>")
	response.write("is_capital_sized: "+str(fit.ship.attrs[1785])+"<br>")
	response.write("nos override (nos as in.. gas?): "+str(fit.ship.attrs[1945])+"<br>")
	response.write("speed factor: "+str(fit.ship.attrs[20])+"<br>")






	return response
