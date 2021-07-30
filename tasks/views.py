from django.db.models.base import Model
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import Project, Task

# Create your views here.


class ProjectList(ListView):
    template_name = "tasks/project_list_view.html"
    model = Project
    context_object_name = "projects"


class TaskListView(ListView):
    template_name = "tasks/tasks_list_view.html"
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(project=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        print("context", context)
        return context
