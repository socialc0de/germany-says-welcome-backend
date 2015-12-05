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
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authviews


urlpatterns = [
    url(r'^faq/by-audience/(?P<audience>[0-9]+)/$', views.QuestionByAudienceList.as_view()),
    url(r'^faq/by-county/(?P<county>[0-9]+)/$', views.QuestionByCountyList.as_view()),
    url(r'^poi/by-audience/(?P<audience>[0-9]+)/$', views.POIByAudienceList.as_view()),
    url(r'^poi/by-county/(?P<county>[0-9]+)/$', views.POIByCountyList.as_view()),
    url(r'^phrasecategories/by-language/(?P<language>[a-z]+)/$', views.PhraseCategoryByLanguageList.as_view()),
    url(r'^phrasebook/by-category/(?P<categories>[0-9]+)/$', views.PhraseByCategoryList.as_view()),
    url(r'^api-token-auth/', authviews.obtain_auth_token)
]
