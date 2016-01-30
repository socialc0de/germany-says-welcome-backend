from backend.models import Question
from backend.serializers import *
from rest_framework import generics, viewsets
from django.contrib.auth.models import User
from rest_framework import permissions
from backend.permissions import IsAdminOrReadOnly, PostAllowed
from rest_framework import filters
from rest_framework_gis.filters import InBBoxFilter
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import smtplib
from backend.exceptions import ServiceUnavailable
from django.conf import settings
from rest_framework_extensions.mixins import CacheResponseAndETAGMixin
from rest_framework_extensions.etag.decorators import etag

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
class QuestionByCountyList(APIView):
    @etag()
    def get(self, request, county, format=None):
        questions = Question.objects.filter(county=county).all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class QuestionByAudienceList(APIView):
    @etag()
    def get(self, request, audience, format=None):
        questions = Question.objects.filter(audiences=audience).all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class QuestionByCategoryList(APIView):
    @etag()
    def get(self, request, category, format=None):
        questions = Question.objects.filter(categories=category).all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class QuestionViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (PostAllowed, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('question',)
    def create(self, request, *args, **kwargs):
        langs = request.data['translations'].keys()
        questions = [question_pair['question'] for question_pair in request.data['translations'].values()]
        sender = 'question-sender@germany-says-welcome.de'
        receivers = ['frage@germany-says-welcome.de']
        message = "From: new_question@germany-says-welcome.de\n"
        message += "To: " + ", ".join(receivers) + "\n"
        message += "Subject: [" + " ".join(langs) + "] New Question : "+questions[0]+"\n\n"
        message += "\n".join(questions)
        try:
            with smtplib.SMTP(settings.SMTP_HOST) as smtpObj:
                serializer = UnansweredQuestionSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    smtpObj.starttls()
                    smtpObj.ehlo()
                    smtpObj.login(settings.SMTP_USER, settings.SMTP_PASS)
                    smtpObj.sendmail(sender, receivers, message)
                    serializer.save()
                else:
                    raise ValidationError('This data in invalid. Hint: did you send empty questions?')
                return Response(serializer.data)
        except smtplib.SMTPException:
            raise ServiceUnavailable("Couldn't store question")



class POIViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = POI.objects.all()
    serializer_class = POISerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly,)
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, )

class POIByCountyList(APIView):
    @etag()
    def get(self, request, county, format=None):
        questions = POI.objects.filter(county=county).all()
        serializer = POISerializer(questions, many=True)
        return Response(serializer.data)

class POIByAudienceList(APIView):
    @etag()
    def get(self, request, audience, format=None):
        questions = POI.objects.filter(audiences=audience).all()
        serializer = POISerializer(questions, many=True)
        return Response(serializer.data)

class POIByCategoryList(CacheResponseAndETAGMixin, ListAPIView):
    filter_backends = (InBBoxFilter,)
    serializer_class = POISerializer
    def get_queryset(self):
        category = self.kwargs['category']
        queryset = POI.objects.filter(categories=category).all()
        return queryset

class PhraseViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = Phrase.objects.all()
    serializer_class = PhraseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly,)
    def perform_create(self, serializer):
        if "." not in self.request.data['text_id'] and "/" not in self.request.data['text_id']:
            serializer.save(text_id=self.request.data['text_id'])
        else:
            raise ValidationError("Field text_id cannot contain . or /")

class UserViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

class AudienceViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer
    permission_classes = (IsAdminOrReadOnly,)
# this could be simplyfied
class FAQCategoryViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

class POICategoryViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = POICategory.objects.all()
    serializer_class = POICategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
class PhraseCategoryViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = PhraseCategory.objects.all()
    serializer_class = PhraseCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

class PhraseCategoryByLanguageList(APIView):
    @etag()
    def get(self, request, language, format=None):
        categories = PhraseCategory.objects.language(language).all()
        serializer = PhraseCategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)
class PhraseByCategoryList(APIView):
    @etag()
    def get(self, request, category, format=None):
        phrases = Phrase.objects.filter(category_id=category).all()
        serializer = PhraseSerializer(phrases, many=True, context={'request': request})
        return Response(serializer.data)
class EmergencyNumberViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = EmergencyNumber.objects.all()
    serializer_class = EmergencyNumberSerializer
    permission_classes = (IsAdminOrReadOnly,)