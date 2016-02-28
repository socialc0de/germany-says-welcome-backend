from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.defaultfilters import slugify
from hvad.forms import TranslatableModelForm
from django import forms
from workflow.forms import get_TranslatableGSWModelForm_from_model
class TranslationPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = "backend.can_translate"


class ReviewPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = "backend.can_translate"


class PublishPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = "backend.can_publish"


class ModelNameContextMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model.__name__
        context['model_name'] = slugify(self.model._meta.verbose_name)
        return context


class TranslatableFormMixin():
    def get_form_class(self):
        return get_TranslatableGSWModelForm_from_model(self.model)


class GSWMixin(TranslatableFormMixin, ModelNameContextMixin):
    paginate_by = 50