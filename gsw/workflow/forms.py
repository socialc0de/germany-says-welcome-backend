from hvad.forms import TranslatableModelForm
from django import forms

def get_TranslatableGSWModelForm_from_model(model_cls):
    class TranslatableGSWModelForm(TranslatableModelForm):
        class Meta:
            exclude = ["state"]
            model = model_cls
        language_code = forms.ChoiceField(choices=(('de', 'German'), ('en', 'English'), ('ar', 'Arabic'), ('fr', 'French')))
    return TranslatableGSWModelForm