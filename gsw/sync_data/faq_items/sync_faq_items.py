import requests
import random
import django
django.setup()
from backend.models import Question, Audience

from bs4 import BeautifulSoup


def clean_wordpress_content(content):
    return ''.join(BeautifulSoup(content).findAll(text=True)) 

langs = ["en","de","fr","ar"]
questions = {}
for lang in langs:
	faq_req = requests.get("http://dev-admin.germany-says-welcome.de/wp-json/wp/v2/faq?lang=%s"%lang)
	data = faq_req.json()
	for question in data:
		if question['original_id'] is not None:
			if question['original_id'] not in questions:
				questions[question['original_id']] = {"translations":{}}
			if lang not in questions[question['original_id']]['translations']:
				questions[question['original_id']]['translations'][lang] = {}
			questions[question['original_id']]['cat_ids'] = []
			catreq = requests.get("http://dev-admin.germany-says-welcome.de/wp-json/wp/v2/faq/%s/faq_cat"%question['original_id'])
			for cat in catreq.json():
				questions[question['original_id']]['cat_ids'].append(cat['original_id'])
			
			questions[question['original_id']]['translations'][lang]['question'] = clean_wordpress_content(question['title']['rendered'])
			questions[question['original_id']]['translations'][lang]['answer'] = clean_wordpress_content(question['content']['rendered'])
			questions[question['original_id']]['id'] = int(question['original_id'])
			questions[question['original_id']]['county'] = 5
			questions[question['original_id']]['audiences'] = [Audience.objects.get(id=random.randint(1,3))]
entries_to_delete = Question.objects.all()
for question_id in questions:
	entries_to_delete = entries_to_delete.exclude(id=question_id)
	entries = Question.objects.language('all').filter(id=question_id)
	if len(entries) == 0:
		entry = Question(id=question_id)
		entry.county = questions[question_id]['county']
		entry.audiences = []
		entry.save()
	for language in questions[question_id]['translations']:
		if language in Question.objects.get(id=question_id).get_available_languages():
			entry = Question.objects.language(language).get(id=question_id)
		else:
			entry = Question.objects.get(id=question_id).translate(language)
		entry.question = questions[question_id]['translations'][language]['question']
		entry.answer = questions[question_id]['translations'][language]['answer']
		entry.county = questions[question_id]['county']
		entry.audiences = questions[question_id]['audiences']
		entry.save()
		
entries_to_delete.delete()