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
    model_class = None
    url_field = None
    url_model_field = None

    def get_queryset(self):
        assert self.model_class is not None, "You need to override model_class."
        assert self.url_field is not None, "You need to override url_field."
        assert self.url_model_field is not None, "You need to override url_model_field."

        filter_value = self.kwargs[self.url_field]
        model_field = self.url_model_field if self.url_model_field is not None else self.url_field
        filter_kwargs = {model_field: filter_value}
        queryset = self.model_class.objects.filter(**filter_kwargs).all()
        return queryset


class QuestionFilteredListView(FilteredListView):
    serializer_class = QuestionSerializer
    model_class = Question


class POIFilteredListView(FilteredListView):
    serializer_class = POISerializer
    model_class = POI
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter,)


class GSWDefaultViewSet(CacheResponseAndETAGMixin, viewsets.ModelViewSet):
    model_class = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly,)

    def get_queryset(self):
        assert self.model_class is not None, "You need to override model_class"
        queryset = self.model_class.objects.all()
        return queryset

    def get_serializer_class(self):
        assert self.model_class is not None, "You need to override model_class"
        serializer_name = "%sSerializer" % self.model_class.__name__
        return globals()[serializer_name]


#view sets
class PhraseViewSet(GSWDefaultViewSet):
    model_class = Phrase

    def perform_create(self, serializer):
        if "." not in self.request.data['text_id'] and "/" not in self.request.data['text_id']:
            serializer.save(text_id=self.request.data['text_id'])
        else:
            raise ValidationError("Field text_id cannot contain . or /")


class UserViewSet(GSWDefaultViewSet):
    model_class = User
    permission_classes = (permissions.IsAdminUser,)


class AudienceViewSet(GSWDefaultViewSet):
    model_class = Audience


class FAQCategoryViewSet(GSWDefaultViewSet):
    model_class = FAQCategory


class POICategoryViewSet(GSWDefaultViewSet):
    model_class = POICategory


class PhraseCategoryViewSet(GSWDefaultViewSet):
    model_class = PhraseCategory


class EmergencyNumberViewSet(GSWDefaultViewSet):
    model_class = EmergencyNumber


class POIViewSet(GSWDefaultViewSet):
    model_class = POI
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter, )


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


# listviews
# questions listviews
class QuestionByCountyList(QuestionFilteredListView):
    url_field = "county"
    url_model_field = "county"


class QuestionByAudienceList(QuestionFilteredListView):
    url_field = "audience"
    url_model_field = "audiences"


class QuestionByCategoryList(QuestionFilteredListView):
    url_field = "category"
    url_model_field = "categories"


# poi listviews
class POIByCountyList(POIFilteredListView):
    url_field = "county"


class POIByAudienceList(POIFilteredListView):
    url_field = "audience"
    url_model_field = "audiences"


class POIByCategoryList(POIFilteredListView):
    url_field = "category"
    url_model_field = "categories"


# phrase listviews
class PhraseCategoryByLanguageList(CacheResponseAndETAGMixin, ListAPIView):
    serializer_class = PhraseCategorySerializer

    def get_queryset(self):
        language = self.kwargs['language']
        queryset = PhraseCategory.objects.language(language).all()
        return queryset


class PhraseByCategoryList(FilteredListView):
    model_class = Phrase
    serializer_class = PhraseSerializer
    url_field = "category"
    url_model_field = "category_id"