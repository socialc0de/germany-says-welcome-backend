from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView
from workflow.viewsets import GSWModelViewSet
from backend.models import Audience, Question, FAQCategory, POI, POICategory, Phrase, PhraseCategory, EmergencyNumber
from workflow.views import IndexView
from workflow.constants import MODELS
"""urlpatterns = patterns('',
    url('', include(GSWModelViewSet(Audience).urls)),
    url('', include(GSWModelViewSet(FAQCategory).urls)),
    url('', include(GSWModelViewSet(FAQCategory).urls)),
    url('', include(GSWModelViewSet(FAQCategory).urls)),
    url('', include(GSWModelViewSet(FAQCategory).urls)),
    url('', include(GSWModelViewSet(FAQCategory).urls)),
    url('', include(GSWModelViewSet(FAQCategory).urls)),
)"""

urlpatterns = [url(r'^$', IndexView.as_view(), name="home")]
for model in MODELS:
	urls = GSWModelViewSet(model).urls
	urlpatterns.append(url('', include(urls)))
	print(urls)
#url('', include(GSWModelViewSet(FAQCategory).urls)),
#url('', include(GSWModelViewSet(Audience).urls)),
#import pdb;pdb.set_trace()
"""url(r'^audiences/$', views.AudienceListView.as_view(), name="audiences-list"),
    url(r'^audiences/new/$', views.NewAudienceView.as_view(), name="audience-new"),
    url(r'^audiences/(?P<pk>[0-9]+)/$', views.AudienceDetailView.as_view(), name="audience-details"),
    url(r'^audiences/(?P<pk>[0-9]+)/edit/(?P<language>[a-z-]+)/$', views.AudienceEditView.as_view(), name="audience-edit"),
    url(r'^audiences/(?P<pk>[0-9]+)/review/$', views.AudienceReviewView.as_view(), name="audience-review"),
	url(r'^audiences/(?P<pk>[0-9]+)/publish/$', views.AudiencePublishView.as_view(), name="audience-publish"),
    url(r'^audiences/reviewed/$', views.AudienceReviewedView.as_view(), name="audiences-reviewed"),
    url(r'^audiences/published/$', views.AudiencePublishedView.as_view(), name="audiences-published"),
    url(r'^audiences/not_reviewed/$', views.AudienceNotReviewedView.as_view(), name="audiences-not-reviewed"),"""