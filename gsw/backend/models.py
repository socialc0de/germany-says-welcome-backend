from django.contrib.gis.db import models
from hvad.models import TranslatableModel, TranslatedFields

class Audience(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256)
    )
    def __str__(self):
        return self.name

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256)
    )
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
    categories = models.ManyToManyField(Category)
    translations = TranslatedFields(
        question = models.CharField(max_length=500),
        answer = models.CharField(max_length=500)
    )

class POI(TranslatableModel):
    owner = models.ForeignKey('auth.User', related_name='pois')
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20)
    location = models.PointField()
    county = models.IntegerField()
    translations = TranslatedFields(
        description = models.CharField(max_length=500)
    )

class Phrase(TranslatableModel):
    owner = models.ForeignKey('auth.User', related_name='phrases')
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(PhraseCategory)
    text_id = models.CharField(max_length=200)
    translations = TranslatedFields(
        phrase = models.CharField(max_length=200)
    )