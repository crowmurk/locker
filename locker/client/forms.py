from django import forms
from django.forms.widgets import HiddenInput

from .models import Client, Branch


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('slug', )


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'
        widgets = {'client': HiddenInput()}
