from django.db.models.base import Model
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, DeleteView
from .models import Project, Task
from django.urls.base import reverse_lazy


# Create your views here.


class ProjectList(ListView):
    template_name = "tasks/project_list_view.html"
    model = Project
    context_object_name = "projects"


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ("name",)
    template_name = "tasks/edit_project_view.html"
    pk_url_kwarg = "pk"
    context_object_name = "project"

    def form_valid(self, form):
        project = form.save()
        return redirect(
            "tasks:list_project",
        )


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("tasks:list_project")
    template_name = "tasks/delete_project_view.html"
    pk_url_kwarg = "pk"
    context_object_name = "project"


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
