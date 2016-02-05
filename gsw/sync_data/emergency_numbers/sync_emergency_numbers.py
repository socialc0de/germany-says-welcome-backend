import requests
import random
import django
django.setup()
from backend.models import EmergencyNumber

from bs4 import BeautifulSoup


def clean_wordpress_content(content):
    return ''.join(BeautifulSoup(content).findAll(text=True)) 

langs = ["en","de","fr","ar"]
questions = {}
for lang in langs:
	faq_req = requests.get("http://dev-admin.germany-says-welcome.de/wp-json/wp/v2/emergency?lang=%s"%lang)
	data = faq_req.json()
	for question in data:
		if question['original_id'] is not None:
			if question['original_id'] not in questions:
				questions[question['original_id']] = {"translations":{}}
			if lang not in questions[question['original_id']]['translations']:
				questions[question['original_id']]['translations'][lang] = {}
			questions[question['original_id']]['cat_ids'] = []
			questions[question['original_id']]['county'] = "000000000"
			for term in question['_links']['terms']:
				if term['taxonomy'] == "emergency_county":
					questions[question['original_id']]['county'] = [item['name'] for item in term['data']][0]
					#print(questions[question['original_id']]['cat_ids'])
			questions[question['original_id']]['translations'][lang]['question'] = clean_wordpress_content(question['title']['rendered'])
			questions[question['original_id']]['translations'][lang]['answer'] = clean_wordpress_content(question['content']['rendered'])
			questions[question['original_id']]['id'] = int(question['original_id'])
			questions[question['original_id']]['number'] = question['number']
entries_to_delete = EmergencyNumber.objects.all()
for question_id in questions:
	entries_to_delete = entries_to_delete.exclude(id=question_id)
	entries = EmergencyNumber.objects.language('all').filter(id=question_id)
	if len(entries) == 0:
		entry = EmergencyNumber(id=question_id)
		entry.county = questions[question_id]['county']
		entry.audiences = []
		entry.save()
	for language in questions[question_id]['translations']:
		if language in EmergencyNumber.objects.get(id=question_id).get_available_languages():
			entry = EmergencyNumber.objects.language(language).get(id=question_id)
		else:
			entry = EmergencyNumber.objects.get(id=question_id).translate(language)
		entry.question = questions[question_id]['translations'][language]['question']
		entry.answer = questions[question_id]['translations'][language]['answer']
		entry.county = questions[question_id]['county']
		entry.number = questions[question_id]['number']
		entry.save()
		
entries_to_delete.delete()