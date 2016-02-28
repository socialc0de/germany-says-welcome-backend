from django.contrib import admin
from hvad.admin import TranslatableAdmin
# Register your models here.
import backend.models as models
models_to_register = [models.Audience, models.FAQCategory, models.POICategory, models.PhraseCategory, models.Question, models.UnansweredQuestion, models.POI, models.Phrase, models.EmergencyNumber]
for model in models_to_register:
	admin.site.register(model, TranslatableAdmin)