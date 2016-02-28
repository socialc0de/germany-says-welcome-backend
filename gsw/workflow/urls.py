from django.conf.urls import url, include
from workflow.viewsets import GSWModelViewSet
from workflow.views import IndexView
from workflow.constants import MODELS

urlpatterns = [url(r'^$', IndexView.as_view(), name="home")]
for model in MODELS:
	urls = GSWModelViewSet(model).urls
	urlpatterns.append(url('', include(urls)))