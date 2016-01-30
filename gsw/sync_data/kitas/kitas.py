import requests
import random
import csv
from os import sys, path; sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from tools import gemeinden, get_or_create_category
import django
django.setup()
from backend.models import POI, POICategory
from backend.serializers import POISerializer

translations = {"en":{"name":"Daycare"},"de":{"name":"Kindertagesstätten"},"ar":{"name":"الرعاية النهارية"},"fr":{"name":"Garderie"}}
category_id, category = get_or_create_category("kitas", translations)

entries_to_delete = POI.objects.all()
entries_to_delete.delete()
with open("kitas.csv", encoding='latin-1') as csvfile:
    with open("kitas_kaputt.csv", "w", encoding="latin-1") as errorfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        csvwriter = csv.writer(errorfile, delimiter=';',quotechar='"',)
        next(csvreader, None) # skip header
        for row in csvreader:
            req = requests.get("http://nominatim.germany-says-welcome.de/search/{1}, {2}?format=json&addressdetails=1".format(*row))
            data = req.json()
            if len(data) > 1:
                for item in data:
                    if item["type"] == "kindergarten":
                        data = item
                        break
                else:
                    print("Search for {1}, {2} gave more than one result of which none was a kindergarten.".format(*row))
                    csvwriter.writerow(row)
                    continue
            elif len(data) < 1:
                print("Search for {1}, {2} gave less than one result.".format(*row))
                csvwriter.writerow(row)
                continue
            else:
                data = data[0]
            if 'county' in data['adress'] and data['address']['county'] in gemeinden:
                county = gemeinden[data['address']['county']]
            else:
                print("No county id for %s"%data['address']['county'])
                csvwriter.writerow(row)
                county = "05111000"
            poi = {"translations":{}}
            for language in translations:
                poi["translations"][language] = {}
                poi["translations"][language]['description'] = "{0}\n{1}, {2} {3}".format(*row)
            #poi['id'] = feature['properties']['point_id']
            poi['county'] = county
            poi['location'] = "POINT({0} {1})".format(data['lat'],data['lon'])
            poi['audiences'] = set([random.randint(1,3),random.randint(1,3)])
            poi['categories'] = [category_id]
            poi_serialized = POISerializer(data=poi)
            if poi_serialized.is_valid():
                poi = poi_serialized.save()
                print("Imported {0}, {1}, {2} {3} with id {4}".format(*row[0:4],poi.id))
            else:
                import pdb;pdb.set_trace()