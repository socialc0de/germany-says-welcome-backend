from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.defaultfilters import slugify
from hvad.forms import TranslatableModelForm
from django import forms
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
        class TranslatableGSWModelForm(TranslatableModelForm):
            class Meta:
                exclude = ["state"]
                model = self.model
            language_code = forms.ChoiceField(choices=(('de', 'German'), ('en', 'English'), ('ar', 'Arabic'), ('fr', 'French')))
        return TranslatableGSWModelForm


class GSWMixin(TranslatableFormMixin, ModelNameContextMixin):
    pass