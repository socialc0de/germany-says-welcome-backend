from backend.models import Question
from backend.serializers import *
from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from rest_framework import permissions
from backend.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, PostAllowed
from rest_framework import filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
class QuestionByCountyList(APIView):
    def get(self, request, county, format=None):
        questions = Question.objects.filter(county=county).all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class QuestionByAudienceList(APIView):
    def get(self, request, audience, format=None):
        questions = Question.objects.filter(audiences=audience).all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('question',)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class POIViewSet(viewsets.ModelViewSet):
    queryset = POI.objects.all()
    serializer_class = POISerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class POIByCountyList(APIView):
    def get(self, request, county, format=None):
        questions = POI.objects.filter(county=county).all()
        serializer = POISerializer(questions, many=True)
        return Response(serializer.data)

class POIByAudienceList(APIView):
    def get(self, request, audience, format=None):
        questions = POI.objects.filter(audiences=audience).all()
        serializer = POISerializer(questions, many=True)
        return Response(serializer.data)

class PhraseViewSet(viewsets.ModelViewSet):
    queryset = Phrase.objects.all()
    serializer_class = PhraseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        if "." not in self.request.data['text_id'] and "/" not in self.request.data['text_id']:
            serializer.save(owner=self.request.user, text_id=self.request.data['text_id'])
        else:
            raise ValidationError("Field text_id cannot contain . or /")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

class AudienceViewSet(viewsets.ModelViewSet):
    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer
    permission_classes = (IsAdminOrReadOnly,)
# this could be simplyfied
class FAQCategoryViewSet(viewsets.ModelViewSet):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer
    permission_classes = (IsAdminOrReadOnly,PostAllowed)
    def add(self, request, *args):
        print(args)
        
class POICategoryViewSet(viewsets.ModelViewSet):
    queryset = POICategory.objects.all()
    serializer_class = POICategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
class PhraseCategoryViewSet(viewsets.ModelViewSet):
    queryset = PhraseCategory.objects.all()
    serializer_class = PhraseCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

class PhraseCategoryByLanguageList(APIView):
    def get(self, request, language, format=None):
        categories = PhraseCategory.objects.language(language).all()
        serializer = PhraseCategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)
class PhraseByCategoryList(APIView):
    def get(self, request, category, format=None):
        phrases = Phrase.objects.filter(category_id=category).all()
        serializer = PhraseSerializer(phrases, many=True, context={'request': request})
        return Response(serializer.data)
class EmergencyNumberViewSet(viewsets.ModelViewSet):
    queryset = EmergencyNumber.objects.all()
    serializer_class = EmergencyNumberSerializer
    permission_classes = (IsAdminOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)