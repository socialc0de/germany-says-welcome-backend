from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Q
from django.http import HttpResponseRedirect

from workflow.mixins import *
#from workflow.forms import TranslatableGSWModelForm


class GSWNewView(GSWMixin, TranslationPermissionRequiredMixin, CreateView):
    template_name = 'new.html'
    success_url = "../"


class GSWListView(GSWMixin, ListView):
    template_name = 'list.html'
    language_order = ["en", "de", "fr", "ar"]
    def get_queryset(self):
        assert self.language_order != None, "You have to set language_order"
        assert self.model != None, "You have to set model"
        queryset = self.model.objects.language(self.language_order[0]).fallbacks(*self.language_order[1:])
        queryset = self.filter(queryset)
        return queryset
    def filter(self, queryset):
        return queryset


class GSWDetailView(GSWMixin, ListView):
    template_name = 'detail.html'
    pk_field = "pk"
    def get_queryset(self):
        assert self.model != None, "You have to set model"
        pk = self.kwargs.get(self.pk_field)
        queryset = self.model.objects.language("all").filter(pk=pk)
        return queryset


class GSWEditView(GSWMixin, TranslationPermissionRequiredMixin, UpdateView):
    template_name = 'new.html'
    success_url = "../../"
    pk_field = "pk"
    language_field = "language"
    def get_object(self):
        assert self.model != None, "You have to set model"
        pk = self.kwargs.get(self.pk_field)
        lang = self.kwargs.get(self.language_field)
        if lang != "new":
            queryset = self.model.objects.language(lang).filter(pk=pk).get()
            return queryset
        else:
            queryset = self.model.objects.language("all").filter(pk=pk)
            return queryset[0].translate("tmp")


    def get_initial(self, **kwargs):
        initial = super().get_initial(**kwargs)
        lang = self.kwargs.get(self.language_field)
        initial['language_code'] = lang
        if lang == "new":
            initial = {}
        return initial


class GSWModifyConfirmView(GSWMixin, ListView):
    template_name = 'confirm-modify.html'
    success_url = "../"
    pk_field = "pk"
    def get_queryset(self):
        assert self.model != None, "You have to set model"
        pk = self.kwargs.get(self.pk_field)
        queryset = self.model.objects.language("all").filter(pk=pk)
        return queryset
    def post(self, *args, **kwargs):
        pk = kwargs.get(self.pk_field)
        obj = self.model.objects.get(pk=pk)
        obj = self.modify(obj)
        obj.save()
        return HttpResponseRedirect(self.success_url)
    def modify(self, obj):
        return obj

class GSWReviewView(ReviewPermissionRequiredMixin, GSWModifyConfirmView):
    def modify(self, obj):
        obj.reviewed()
        return obj


class GSWPublishView(PublishPermissionRequiredMixin, GSWModifyConfirmView):
    def modify(self, obj):
        obj.publish()
        return obj


class GSWReviewedView(GSWListView):
    def filter(self, queryset):
        queryset = queryset.filter(state="reviewed")
        return queryset

class GSWPublishedView(GSWListView):
    def filter(self, queryset):
        queryset = queryset.filter(state="published")
        return queryset

class GSWNotReviewedView(GSWListView):
    def filter(self, queryset):
        queryset = queryset.filter(Q(state="new") | Q(state="translated"))
        return queryset