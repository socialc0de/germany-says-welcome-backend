from rest_framework import serializers
from backend.models import Question, POI, Phrase, Audience, Category, PhraseCategory
from django.contrib.auth.models import User
from hvad.contrib.restframework.serializers import TranslatableModelSerializer, HyperlinkedTranslatableModelSerializer, TranslationsMixin
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer


class QuestionSerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = Question
        exclude = ('owner',)

class POISerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = POI
        exclude = ('owner',)

class PhraseSerializer(TranslationsMixin, HyperlinkedModelSerializer):
    class Meta:
        model = Phrase
        exclude = ('owner',)
        extra_kwargs = {
            'language': {'lookup_field': 'phrase__language'}
        }

class AudienceSerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = Audience

class CategorySerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = Category

class PhraseCategorySerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = PhraseCategory

class UserSerializer(TranslationsMixin, ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    pois = serializers.PrimaryKeyRelatedField(many=True, queryset=POI.objects.all())
    translations = serializers.PrimaryKeyRelatedField(many=True, queryset=Phrase.objects.all())
    phrases = serializers.PrimaryKeyRelatedField(many=True, queryset=Phrase.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'questions', 'pois', 'translations', 'phrases')