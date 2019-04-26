from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from . import get_ships
from ships.models import Invgroups, Invtypes

from eos import *
from eos.item_filter import *

import json

#does outsourcing work?
data_handler = JsonDataHandler('/home/ubuntu/eos/phobos/')  # Folder with Phobos data dump
cache_handler = JsonCacheHandler('/home/ubuntu/eos/cache/eos_tq.json.bz2')
SourceManager.add('tiamat', data_handler, cache_handler, make_default=True)

skill_groups = set(row['groupID'] for row in data_handler.get_evegroups() if row['categoryID'] == 16)
skills = set(row['typeID'] for row in data_handler.get_evetypes() if row['groupID'] in skill_groups)


def index(request):
	response = HttpResponse()
	categorylist = Invgroups.objects.filter(categoryid="6")
	for i in categorylist:
		response.write("<a href='list/"+str(i.groupid)+"'>"+i.groupname+"</a><br>")
	return response

def list(request, groupid):
	response = HttpResponse()
	grouplist = Invtypes.objects.filter(groupid=groupid)
	for i in grouplist:
		if i.published == True:
			response.write("<img src='https://imageserver.eveonline.com/Type/"+str(i.typeid)+"_32.png'><a href='/ships/"+str(i.typeid)+"'>"+str(i.typename)+"</a><br>")
	return response

def detail(request, shipid):
	ship = Invtypes.objects.filter(typeid__exact=shipid)
	for k in ship:
		typename = k.typename
		description = k.description
	template = loader.get_template('ships/detail.html')
	context = {
		'shipid': shipid,
		'shipname': typename,
		'desc': description,
	}

	return HttpResponse(template.render(context, request))

def ajax_spawn(request, shipid):

	fit = Fit()
	fit.ship = Ship(shipid)

	for skill_id in skills:
		fit.skills.add(Skill(skill_id, level=5))

	fit.validate()

	data = { }

	for key,value in fit.ship.attrs.items():
		data.update( { key: value })

	data.update( {
		'pg_out': int(fit.ship.attrs[11]),
		'cpu_out': int(fit.ship.attrs[48]),
		'veloc': int(fit.ship.attrs[37]),
		'sig': int(fit.ship.attrs[552]),
		'scanres': int(fit.ship.attrs[564]),
		'target_range': int(fit.ship.attrs[76]),
		'warp': int(fit.ship.attrs[600]),
		'cargo': int(fit.ship.attrs[38]),
		'cargo_drone': int(fit.ship.attrs[283]),
		'drone_bw': int(fit.ship.attrs[1271]),
		'hi_slot': int(fit.ship.attrs[14]),
		'mid_slot': int(fit.ship.attrs[13]),
		'low_slot': int(fit.ship.attrs[12]),
		'rig_slot': int(fit.ship.attrs[1137]),
		'agil': int(fit.ship.attrs[70]),
	})

	return JsonResponse(data)

def ajax_modules(request, shipid):

	data = {
	'test': 'test'
	}

	return JsonResponse(data)
