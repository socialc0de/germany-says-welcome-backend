import requests
import random
import csv
from os import sys, path; sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import django
django.setup()
from tools import gemeinden, get_or_create_category
from backend.models import POI, POICategory
from backend.serializers import POISerializer

translations = {"en":{"name":"Correspondents of trafficking"},"de":{"name":"Anlaufstellen bei Menschenhandel"},"ar":{"name":"مراسلي الاتجار"},"fr":{"name":"Correspondants de la traite"}}
category_id, category = get_or_create_category("erstaufnameeinrichtungen", translations)

entries_to_delete = POI.objects.filter(categories=category).all()
entries_to_delete.delete()
with open("erstaufnameeinrichtungen.csv", encoding='latin-1') as csvfile:
    with open("erstaufnameeinrichtungen_kaputt.csv", "w", encoding="latin-1") as errorfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        csvwriter = csv.writer(errorfile, delimiter=';',quotechar='"',)
        next(csvreader, None) # skip header
        next(csvreader, None) # skip emptry line
        for row in csvreader:
            req = requests.get("http://nominatim.germany-says-welcome.de/search/{1}?format=json&addressdetails=1".format(*row))
            data = req.json()
            if len(data) < 1:
                print("Search for {0}, {1} gave less than one result.".format(*row))
                csvwriter.writerow(row)
                continue
            else:
                data = data[0]
            if 'county' in data['address'] and data['address']['county'] in gemeinden:
                county = gemeinden[data['address']['county']]
            else:
                print("No county id for {0!s}".format(row[0]))
                csvwriter.writerow(row)
                county = "00000000"
            poi = {"translations":{}}
            for language in translations:
                poi["translations"][language] = {}
                poi["translations"][language]['description'] = "{0}".format(*row)
            #poi['id'] = feature['properties']['point_id']
            poi['county'] = county
            poi['location'] = "POINT({0} {1})".format(data['lat'],data['lon'])
            poi['audiences'] = set([random.randint(1,3),random.randint(1,3)])
            poi['categories'] = [category_id]
            poi_serialized = POISerializer(data=poi)
            if poi_serialized.is_valid():
                poi = poi_serialized.save()
                print("Imported {0}, {1} with id {2}".format(*row[0:2],poi.id))
            else:
                print("Couldn't import {0}, {1}".format(*row))
                csvwriter.writerow(row)