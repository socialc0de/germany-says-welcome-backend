"""gsw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import include

from rest_framework.urlpatterns import format_suffix_patterns
from backend import views
from backend.routers import GSWDefaultRouter
from backend import urls
from gsw import settings

apirouter = GSWDefaultRouter()
apirouter.register(r'audiences', views.AudienceViewSet)
apirouter.register(r'faq', views.QuestionViewSet)
apirouter.register(r'faqcategories', views.FAQCategoryViewSet)
apirouter.register(r'poi', views.POIViewSet)
apirouter.register(r'poicategories', views.POICategoryViewSet)
apirouter.register(r'users', views.UserViewSet)
apirouter.register(r'phrasebook', views.PhraseViewSet)
apirouter.register(r'phrasecategories', views.PhraseCategoryViewSet)
apirouter.register(r'emergencynumbers', views.EmergencyNumberViewSet)
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(apirouter.urls)),
    url(r'^api/', include(urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
    ]
