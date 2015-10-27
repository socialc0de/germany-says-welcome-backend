from rest_framework import serializers
from backend.models import Question, POI, Phrase, PhraseCollection
from django.contrib.auth.models import User

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ('owner',)

class POISerializer(serializers.ModelSerializer):
    class Meta:
        model = POI
        exclude = ('owner',)

class PhraseCollectionSerializer(serializers.HyperlinkedModelSerializer):
    translations = serializers.StringRelatedField(many=True)
    class Meta:
        exclude = ('owner',)
        model = PhraseCollection
        extra_kwargs = {
            'language': {'lookup_field': 'phrase__language'}
        }

class PhraseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phrase
        exclude = ('owner',)

class UserSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    pois = serializers.PrimaryKeyRelatedField(many=True, queryset=POI.objects.all())
    translations = serializers.PrimaryKeyRelatedField(many=True, queryset=Phrase.objects.all())
    phrases = serializers.PrimaryKeyRelatedField(many=True, queryset=PhraseCollection.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'questions', 'pois', 'translations', 'phrases')