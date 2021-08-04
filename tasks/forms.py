from django.forms import ModelForm, fields
from django import forms
from .models import *


class ProjectForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add new project..."})
    )

    class Meta:
        model = Project
        fields = "__all__"
