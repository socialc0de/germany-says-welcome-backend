from django.views.generic.base import TemplateView
from workflow.metaviews import GSWNewView, GSWListView, GSWDetailView, GSWEditView, GSWReviewView, GSWPublishView, GSWReviewedView, GSWPublishedView, GSWNotReviewedView
from workflow.constants import MODELS
from django.template.defaultfilters import slugify
# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        models = [(model._meta.verbose_name, slugify(model._meta.verbose_name_plural)) for model in MODELS]
        context['models'] = models
        return context