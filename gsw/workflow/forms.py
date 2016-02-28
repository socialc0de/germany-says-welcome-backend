from hvad.forms import TranslatableModelForm
from django import forms
from material import *
from backend.models import Audience
"""class NewAudienceForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    language = forms.ChoiceField(choices=(('de', 'German'), ('en', 'English'), ('ar', 'Arabic'), ('fr', 'French')))
    
    layout = Layout('name', 'description', 'language')"""
"""
class TranslatableGSWModelForm(TranslatableModelForm):

    class Meta:
        exclude = ["state"]
    language_code = forms.ChoiceField(choices=(('de', 'German'), ('en', 'English'), ('ar', 'Arabic'), ('fr', 'French')))
    """