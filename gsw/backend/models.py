from django.contrib.gis.db import models

class Question(models.Model):
    owner = models.ForeignKey('auth.User', related_name='questions')
    created = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    language = models.CharField(max_length=2)
    county = models.IntegerField()

class POI(models.Model):
    owner = models.ForeignKey('auth.User', related_name='pois')
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    location = models.PointField()
    county = models.IntegerField()

class PhraseCollection(models.Model):
    owner = models.ForeignKey('auth.User', related_name='phrases')
    created = models.DateTimeField(auto_now_add=True)
    english_phrase = models.CharField(max_length=200)
    def __str__(self):
        return '%s' % self.english_phrase

class Phrase(models.Model):
    owner = models.ForeignKey('auth.User', related_name='translations')
    translation = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=2)
    collection = models.ForeignKey('PhraseCollection', related_name='translations')


