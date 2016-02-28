from django.contrib.gis.db import models
from hvad.models import TranslatableModel, TranslatedFields
from django_fsm import FSMField, transition

#own classes

class GSWModel(TranslatableModel):
    state = FSMField(default='new', choices=[("new", "Object in Translation"), ("translated", "Object needs Review"), ("reviewed", "Object can be published"), ("published", "Object is public")])
    @transition(field=state, source='new', target='translated',
        permission=lambda user: user.has_perm('gsw.can_translate'))
    def translated(self):
        pass
    @transition(field=state, source=['new', 'translated'], target='reviewed',
        permission=lambda user: user.has_perm('gsw.can_review'))
    def reviewed(self):
        pass
    @transition(field=state, source='reviewed', target='published',
        permission=lambda user: user.has_perm('gsw.can_publish'))
    def publish(self):
        pass
    class Meta:
        abstract = True
        permissions = (
            ("can_translate", "Can translate objects."),
            ("can_review", "Can review an objects."),
            ("can_publish", "Can publish objects (only very few people should be allowed to do that)"),
        )


class GSWCategory(GSWModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256)
    )
    def __str__(self):
        return self.name
    class Meta:
        abstract = True


class Audience(GSWModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=256),
        description = models.CharField(max_length=256)
    )
    #def __str__(self):
    #    return self.name


class FAQCategory(GSWCategory):
    image = models.ImageField(upload_to='./', null=True)
    translations = TranslatedFields()

class POICategory(GSWCategory):
    text_id = models.CharField(max_length=200, blank=False)
    icon = models.ImageField(upload_to='./', null=True)
    translations = TranslatedFields()

class PhraseCategory(GSWCategory):
    translations = TranslatedFields()


class Question(GSWModel):
    county = models.CharField(max_length=8)
    audiences = models.ManyToManyField(Audience)
    categories = models.ManyToManyField(FAQCategory)
    translations = TranslatedFields(
        question = models.CharField(max_length=500),
        answer = models.CharField(max_length=500)
    )
class UnansweredQuestion(GSWModel):
    county = models.CharField(max_length=8)
    question = models.CharField(max_length=500, null=True),
    translations = TranslatedFields(
        question = models.CharField(max_length=500),
    )

class POI(GSWModel):
    location = models.PointField()
    county = models.CharField(max_length=8)
    audiences = models.ManyToManyField(Audience)
    categories = models.ManyToManyField(POICategory)
    translations = TranslatedFields(
        description = models.CharField(max_length=500)
    )

class Phrase(GSWModel):
    category = models.ForeignKey(PhraseCategory, related_name='phrases')
    text_id = models.CharField(max_length=200, primary_key=True, blank=False)
    translations = TranslatedFields(
        phrase = models.CharField(max_length=200)
    )

class EmergencyNumber(GSWModel):
    number = models.CharField(max_length=30, blank=False)
    county = models.CharField(max_length=8)
    translations = TranslatedFields(
        name = models.CharField(max_length=100),
        description = models.CharField(max_length=500)
    )