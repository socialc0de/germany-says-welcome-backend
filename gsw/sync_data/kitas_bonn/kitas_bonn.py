import requests
import random
import json
from os import sys, path; sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from pyproj import Proj, transform
import django
django.setup()
from backend.models import POI, POICategory
from backend.serializers import POISerializer

translations = {"en":{"name":"Daycare"},"de":{"name":"Kindertagesstätten"},"ar":{"name":"الرعاية النهارية"},"fr":{"name":"Garderie"}}

county = "05314000"
categories = POICategory.objects.language('all').filter(text_id="kitas")
if len(categories) == 0:
	category = POICategory(text_id="kitas")
	category.save()
else:
	category = categories[0]
category_id = category.id
for language in translations:
	if language in POICategory.objects.get(id=category_id).get_available_languages():
		category = POICategory.objects.language(language).get(id=category_id)
	else:
		category = POICategory.objects.get(id=category_id).translate(language)
	category.name = translations[language]['name']
	category.save()
entries_to_delete = POI.objects.all()
entries_to_delete.delete()
with open("kitas_bonn.geojson", encoding='latin-1') as jsonfile:
	data = json.load(jsonfile)
	for feature in data['features']:
		poi = {"translations":{}}
		for language in translations:
			poi["translations"][language] = {}
			poi["translations"][language]['description'] = "{0}\n{1}\n{2}".format(feature['properties']['name'],feature['properties']['adresse'],feature['properties']['plzort'])
		#poi['id'] = feature['properties']['point_id']
		poi['county'] = county
		inProj = Proj(init='epsg:25832')
		outProj = Proj(init='epsg:4326')
		poi['location'] = "POINT({0} {1})".format(*reversed(list(transform(inProj,outProj,*feature['geometry']['coordinates']))))
		poi['audiences'] = set([random.randint(1,3),random.randint(1,3)])
		poi['categories'] = [category_id]
		poi_serialized = POISerializer(data=poi)
		if poi_serialized.is_valid():
			poi_serialized.save()
			print(poi_serialized)
		else:
			import pdb;pdb.set_trace()