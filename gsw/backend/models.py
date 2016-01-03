from django.contrib.gis.db import models
from hvad.models import TranslatableModel, TranslatedFields

class Audience(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256),
        description = models.CharField(max_length=256)
    )
    def __str__(self):
        return self.name

# TODO: use a base model for all categories
class FAQCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256)
    )
    image = models.ImageField(upload_to='faq_categories')
    def __str__(self):
        return self.name

class POICategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256)
    )
    icon = models.ImageField(upload_to='poi_categories')
    def __str__(self):
        return self.name

class PhraseCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256)
    )
    def __str__(self):
        return self.name


class Question(TranslatableModel):
    owner = models.ForeignKey('auth.User', related_name='questions')
    created = models.DateTimeField(auto_now_add=True)
    county = models.IntegerField()
    audiences = models.ManyToManyField(Audience)
    categories = models.ManyToManyField(FAQCategory)
    translations = TranslatedFields(
        question = models.CharField(max_length=500),
        answer = models.CharField(max_length=500)
    )
class UnansweredQuestion(TranslatableModel):
    created = models.DateTimeField(auto_now_add=True)
    county = models.IntegerField()
    question = models.CharField(max_length=500, null=True),
    translations = TranslatedFields(
        question = models.CharField(max_length=500),
    )

class POI(TranslatableModel):
    owner = models.ForeignKey('auth.User', related_name='pois')
    created = models.DateTimeField(auto_now_add=True)
    location = models.PointField()
    county = models.IntegerField()
    audiences = models.ManyToManyField(Audience)
    categories = models.ManyToManyField(POICategory)
    translations = TranslatedFields(
        description = models.CharField(max_length=500)
    )

class Phrase(TranslatableModel):
    owner = models.ForeignKey('auth.User', related_name='phrases')
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(PhraseCategory, related_name='phrases')
    text_id = models.CharField(max_length=200, primary_key=True, blank=False)
    translations = TranslatedFields(
        phrase = models.CharField(max_length=200)
    )

class EmergencyNumber(TranslatableModel):
    owner = models.ForeignKey('auth.User', related_name='numbers')
    created = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length=30, blank=False)
    county = models.IntegerField()
    translations = TranslatedFields(
        name = models.CharField(max_length=100),
        description = models.CharField(max_length=500)
    )