import csv
from backend.models import POI, POICategory
def load_gemeinden():
	gemeinden = {}
	with open("../gemeinden.csv", encoding="utf-8") as csvfile:
		csvreader = csv.reader(csvfile, delimiter=",")
		for row in csvreader:
			gemeindename = row[1].split(",")[0]
			gemeinden[gemeindename] = row[0]
	return gemeinden
gemeinden = load_gemeinden()
def get_or_create_category(textid, translations):
	categories = POICategory.objects.language('all').filter(text_id=textid)
	if len(categories) == 0:
	    category = POICategory(text_id=textid)
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
	return category_id, category