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
import smtplib
from backend.exceptions import ServiceUnavailable
smtp_user = "SMTP USER"
smtp_pwd = "SMTP PASSWORD"
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

class QuestionByCategoryList(APIView):
    def get(self, request, category, format=None):
        questions = Question.objects.filter(category=category).all()
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
    def create(self, request, *args, **kwargs):
        langs = request.data['translations'].keys()
        questions = [question_pair['question'] for question_pair in request.data['translations'].values()]

        sender = 'question-sender@germany-says-welcome.de'
        receivers = ['frage@germany-says-welcome.de']
        message = "From: new_question@germany-says-welcome.de\n"
        message += "To: " + ", ".join(receivers) + "\n"
        message += "Subject: [" + " ".join(langs) + "] New Question : "+questions[0]+"\n\n"
        message += "\n".join(questions)

        with smtplib.SMTP('YOUR MAIL SERVER WITH SUBMISSION PORT HERE') as smtpObj:
            smtpObj.starttls()
            smtpObj.ehlo()
            smtpObj.login(smtp_user, smtp_pwd)
            smtpObj.sendmail(sender, receivers, message)
            return Response(request.data)
        """try:
            smtpObj = smtplib.SMTP('mail.germany-says-welcome.de')
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo
            smtpObj.login(smtp_user, smtp_pwd)
            smtpObj.sendmail(sender, receivers, message)
            return Response(request.data)
        except smtplib.SMTPException:
            raise ServiceUnavailable("Couldn't store question")"""



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
    permission_classes = (IsAdminOrReadOnly,)

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