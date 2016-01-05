import requests
import json
import os
import django
django.setup()
from backend.models import FAQCategory
from django.core.files import File
import filecmp
langs = ["en","de","fr","ar"]
faq_categories = {}
for lang in langs:
	faq_req = requests.get("http://dev-admin.germany-says-welcome.de/wp-json/wp/v2/faq_cat?lang=%s"%lang)
	data = faq_req.json()
	for cat in data:
		if cat['original_id'] is not None:
			if cat['original_id'] not in faq_categories:
				faq_categories[cat['original_id']] = {"translations":{}}
			if lang not in faq_categories[cat['original_id']]['translations']:
				faq_categories[cat['original_id']]['translations'][lang] = {}
			faq_categories[cat['original_id']]['translations'][lang]['name'] = cat['name']
			faq_categories[cat['original_id']]['image_url'] = cat['image_url']
			faq_categories[cat['original_id']]['id'] = int(cat['original_id'])+50

entries_to_delete = FAQCategory.objects.all()
for cat_id in faq_categories:
	entries_to_delete = entries_to_delete.exclude(id=cat_id)
	entries = FAQCategory.objects.language('all').filter(id=cat_id)
	if len(entries) == 0:
		entry = FAQCategory(id=cat_id)
		entry.save()
	for language in faq_categories[cat_id]['translations']:
		if language in FAQCategory.objects.get(id=cat_id).get_available_languages():
			entry = FAQCategory.objects.language(language).get(id=cat_id)
		else:
			entry = FAQCategory.objects.get(id=cat_id).translate(language)
		entry.name = faq_categories[cat_id]['translations'][language]['name']
		entry.save()
	image = requests.get(faq_categories[cat_id]['image_url'])
	image_name = os.path.basename(faq_categories[cat_id]['image_url'])
	with open("/tmp/%s"%image_name, "wb") as f:
		f.write(image.content)
	reopen = open("/tmp/%s"%image_name, "rb")
	if entry.image != "":
		old_image = entry.image.open()
	if reopen != None and (entry.image == "" or reopen.read() != old_image.read()): #slow, please replace in future
		django_file = File(reopen)
		entry.image.save(image_name, django_file)
	entry.save()
		
entries_to_delete.delete()