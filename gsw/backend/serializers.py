from rest_framework import serializers
from backend.models import Question, UnansweredQuestion, POI, Phrase, Audience, FAQCategory, POICategory, PhraseCategory, EmergencyNumber
from django.contrib.auth.models import User
from hvad.contrib.restframework.serializers import TranslatableModelSerializer, HyperlinkedTranslatableModelSerializer, TranslationsMixin
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, ReadOnlyField


class QuestionSerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = Question


class UnansweredQuestionSerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = UnansweredQuestion


class POISerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = POI


class PhraseSerializer(TranslationsMixin, ModelSerializer):
    #id = ReadOnlyField()
    class Meta:
        model = Phrase
        extra_kwargs = {
            'language': {'lookup_field': 'phrase__language'}
        }


class AudienceSerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = Audience


class FAQCategorySerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = FAQCategory


class POICategorySerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = POICategory


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


class EmergencyNumberSerializer(TranslationsMixin, ModelSerializer):
    class Meta:
        model = EmergencyNumber