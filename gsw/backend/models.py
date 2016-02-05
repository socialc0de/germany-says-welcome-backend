from django.contrib.gis.db import models
from hvad.models import TranslatableModel, TranslatedFields


#own classes
class GSWCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256)
    )
    def __str__(self):
        return self.name
    class Meta:
        abstract = True


class Audience(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256),
        description = models.CharField(max_length=256)
    )
    def __str__(self):
        return self.name


class FAQCategory(GSWCategory):
    image = models.ImageField(upload_to='./', null=True)
    translations = TranslatedFields()

class POICategory(GSWCategory):
    text_id = models.CharField(max_length=200, blank=False)
    icon = models.ImageField(upload_to='./', null=True)
    translations = TranslatedFields()

class PhraseCategory(GSWCategory):
    translations = TranslatedFields()


class Question(TranslatableModel):
    county = models.CharField(max_length=8)
    audiences = models.ManyToManyField(Audience)
    categories = models.ManyToManyField(FAQCategory)
    translations = TranslatedFields(
        question = models.CharField(max_length=500),
        answer = models.CharField(max_length=500)
    )
class UnansweredQuestion(TranslatableModel):
    county = models.CharField(max_length=8)
    question = models.CharField(max_length=500, null=True),
    translations = TranslatedFields(
        question = models.CharField(max_length=500),
    )

class POI(TranslatableModel):
    location = models.PointField()
    county = models.CharField(max_length=8)
    audiences = models.ManyToManyField(Audience)
    categories = models.ManyToManyField(POICategory)
    translations = TranslatedFields(
        description = models.CharField(max_length=500)
    )

class Phrase(TranslatableModel):
    category = models.ForeignKey(PhraseCategory, related_name='phrases')
    text_id = models.CharField(max_length=200, primary_key=True, blank=False)
    translations = TranslatedFields(
        phrase = models.CharField(max_length=200)
    )

class EmergencyNumber(TranslatableModel):
    number = models.CharField(max_length=30, blank=False)
    county = models.CharField(max_length=8)
    translations = TranslatedFields(
        name = models.CharField(max_length=100),
        description = models.CharField(max_length=500)
    )