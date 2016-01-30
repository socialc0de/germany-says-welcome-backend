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
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError
from django.conf import settings
import smtplib
from backend.exceptions import ServiceUnavailable
from django.conf import settings
from rest_framework_extensions.mixins import CacheResponseAndETAGMixin
from rest_framework_extensions.etag.decorators import etag

#own classes

class FilteredListView(CacheResponseAndETAGMixin, ListAPIView):
    model = None
    url_field = None
    url_model_field = None
    def get_queryset(self):
        assert self.model is not None, "model should not be None"
        assert self.url_field is not None, "url_field should not be None"
        filter_value = self.kwargs[self.url_field]
        model_field = self.url_model_field if self.url_model_field is not None else self.url_field
        filter_kwargs = {model_field: filter_value}
        queryset = self.model.objects.filter(**filter_kwargs).all()
        return queryset

class QuestionFilteredListView(FilteredListView):
    serializer_class = QuestionSerializer
    model = Question

class POIFilteredListView(FilteredListView):
    serializer_class = POISerializer
    model = POI
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter,)

# question views

class QuestionByCountyList(QuestionFilteredListView):
    url_field = "county"
    url_model_field = "county"

class QuestionByAudienceList(APIView):
    url_field = "audience"
    url_model_field = "audiences"

class QuestionByCategoryList(APIView):
    url_field = "category"
    url_model_field = "categories"

class QuestionViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (PostAllowed, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('question',)
    def create(self, request, *args, **kwargs):
        langs = request.data['translations'].keys()
        questions = [question_pair['question'] for question_pair in
            request.data['translations'].values()]
        sender = 'question-sender@germany-says-welcome.de'
        receivers = ['frage@germany-says-welcome.de']
        message = "From: new_question@germany-says-welcome.de\n"
        message += "To: " + ", ".join(receivers) + "\n"
        message += "Subject: [" + " ".join(langs) + "] New Question : " + questions[0] + "\n\n"
        message += "\n".join(questions)
        try:
            with smtplib.SMTP(settings.SMTP_HOST) as smtpObj:
                serializer = UnansweredQuestionSerializer(data=request.data,
                    context={'request': request})
                if serializer.is_valid():
                    smtpObj.starttls()
                    smtpObj.ehlo()
                    smtpObj.login(settings.SMTP_USER, settings.SMTP_PASS)
                    smtpObj.sendmail(sender, receivers, message)
                    serializer.save()
                else:
                    raise ValidationError('This data in invalid.' +
                        'Hint: did you send empty questions?')
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



class POIByCountyList(POIFilteredListView):
    url_field = "county"

class POIByAudienceList(POIFilteredListView):
    url_field = "audience"
    url_model_field = "audiences"

class POIByCategoryList(POIFilteredListView):
    url_field = "category"
    url_model_field = "categories"

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
class CategoryViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    category_name = None

    def get_queryset(self):
        assert self.category_name is not None, "You need to override category_name"
        category = globals()[self.category_name]
        queryset = category.objects.all()
        return queryset

    def get_serializer_class(self):
        serializer_name = "%sSerializer" % self.category_name
        return globals()[serializer_name]

class FAQCategoryViewSet(CategoryViewSet):
    category_name = "FAQCategory"

class POICategoryViewSet(CategoryViewSet):
    category_name = "POICategory"

class PhraseCategoryViewSet(CategoryViewSet):
    category_name = "PhraseCategory"

class PhraseCategoryByLanguageList(CacheResponseAndETAGMixin, ListAPIView):
    serializer_class = PhraseCategorySerializer
    def get_queryset(self):
        language = self.kwargs['language']
        queryset = PhraseCategory.objects.language(language).all()
        return queryset

class PhraseByCategoryList(FilteredListView):
    model = Phrase
    serializer_class = PhraseSerializer
    url_field = "category"
    url_model_field = "category_id"


class EmergencyNumberViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    queryset = EmergencyNumber.objects.all()
    serializer_class = EmergencyNumberSerializer
    permission_classes = (IsAdminOrReadOnly,)