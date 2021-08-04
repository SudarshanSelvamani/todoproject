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


class TaskForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add new task..."})
    )
    end = forms.DateTimeField(
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Task
        fields = ["text", "tag", "completed"]
