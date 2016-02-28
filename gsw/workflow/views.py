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

"""class NewAudienceView(GSWNewView):
    model = Audience

class AudienceListView(GSWListView):
    model = Audience
    language_order = ["en", "de", "fr", "ar"]

class AudienceDetailView(GSWDetailView):
    model = Audience

class AudienceEditView(GSWEditView):
    model = Audience

class AudienceReviewView(GSWReviewView):
    model = Audience

class AudiencePublishView(GSWPublishView):
    model = Audience

class AudienceReviewedView(GSWReviewedView):
    model = Audience
    language_order = ["en", "de", "fr", "ar"]

class AudiencePublishedView(GSWPublishedView):
    model = Audience
    language_order = ["en", "de", "fr", "ar"]


class AudienceNotReviewedView(GSWNotReviewedView):
    model = Audience
    language_order = ["en", "de", "fr", "ar"]"""


"""class NewAudienceView(TranslationPermissionRequiredMixin, CreateView):
    template_name = 'new_audience.html'
    form_class = NewAudienceForm
    model = Audience
    success_url = "../"

class AudienceListView(ListView):
    model = Audience
    template_name = 'audience_list.html'
    queryset = Audience.objects.language("en").fallbacks().all()


class AudienceDetailView(ListView):
    model = Audience
    template_name = 'audience_detail.html'
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = Audience.objects.language("all").filter(pk=pk)
        return queryset


class AudienceEditView(TranslationPermissionRequiredMixin, UpdateView):
    model = Audience
    template_name = 'new_audience.html'
    form_class = NewAudienceForm
    success_url = "../../"
    def get_object(self):
        pk = self.kwargs.get("pk")
        lang = self.kwargs.get("language")
        if lang != "new":
            queryset = Audience.objects.language(lang).filter(pk=pk).get()
            return queryset
        else:
            queryset = Audience.objects.language("all").filter(pk=pk)
            return queryset[0].translate("tmp")


    def get_initial(self, **kwargs):
        initial = super(AudienceEditView, self).get_initial(**kwargs)
        lang = self.kwargs.get("language")
        initial['language_code'] = lang
        if lang == "new":
            initial = {}
        return initial

class AudienceReviewView(ReviewPermissionRequiredMixin, ListView):
    model = Audience
    template_name = 'audience_review.html'
    fields = []
    success_url = "../../"
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = Audience.objects.language("all").filter(pk=pk)
        return queryset
    def post(self, *args, **kwargs):
        aud = Audience.objects.get(pk=kwargs['pk'])
        aud.reviewed()
        aud.save()
        return HttpResponseRedirect("../")


class AudiencePublishView(ReviewPermissionRequiredMixin, ListView):
    model = Audience
    template_name = 'audience_review.html'
    fields = []
    success_url = "../../"
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = Audience.objects.language("all").filter(pk=pk)
        return queryset
    def post(self, *args, **kwargs):
        aud = Audience.objects.get(pk=kwargs['pk'])
        aud.publish()
        aud.save()
        return HttpResponseRedirect("../")


class AudienceReviewedView(ListView):
    model = Audience
    template_name = 'audience_list.html'
    queryset = Audience.objects.language("en").fallbacks("de", "fr", "ar",).filter(state="reviewed")


class AudienceNotReviewedView(ListView):
    model = Audience
    template_name = 'audience_list.html'
    queryset = Audience.objects.language("en").fallbacks("de", "fr", "ar",).filter(Q(state="new") | Q(state="translated"))"""