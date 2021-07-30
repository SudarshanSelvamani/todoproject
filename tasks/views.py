from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import ListView
from .models import Project

# Create your views here.


class ProjectList(ListView):
    template_name = "tasks/project_list_view.html"
    model = Project
    context_object_name = "projects"
