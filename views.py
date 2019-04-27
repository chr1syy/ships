from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from ships.models import Invgroups, Invtypes, Dgmtypeeffects

from eos import *
from eos.item_filter import *

import json

######## EOS Enginge Settings ########
data_handler = JsonDataHandler('/home/ubuntu/eos/phobos/')
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

	return JsonResponse(data)

def ajax_modules(request, shipid):

	slot = request.GET.get("slot", None)
	low_slots = Dgmtypeeffects.objects.filter(effectid__exact=slot)
	modules = Invtypes.objects.filter(typeid__in=low_slots)
	data = { }
	for module in modules:
		data.update({ module.typeid : module.typename })

	return JsonResponse(data)
