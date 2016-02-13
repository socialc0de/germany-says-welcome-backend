import django
django.setup()
from backend.models import Audience
langs = ["en","de","fr","ar"]
steps = ["Step 1 %s", "Step 2 %s", "Step 3 %s"]
for step in steps:
	audience = Audience()
	for lang in langs:
		audience.translate(lang)
		audience.name = step%lang
		audience.description = step%lang
	audience.save()