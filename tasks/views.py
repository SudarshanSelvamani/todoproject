from django.db.models.base import Model
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, UpdateView, DeleteView, View
from datetime import datetime, timezone
from .models import Project, Task
from django.urls.base import reverse_lazy, reverse
from .forms import TaskForm, ProjectForm


# Create your views here.


class ProjectList(ListView):
    template_name = "tasks/project_list_view.html"
    model = Project
    context_object_name = "projects"


class ProjectCreateView(View):
    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:list_project")
        return render(request, "tasks/create_project_view.html", {"form": form})

    def get(self, request):
        form = ProjectForm()
        return render(request, "tasks/create_project_view.html", {"form": form})


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


class TaskCreateView(View):
    def post(self, request, pk):
        self.project = get_object_or_404(Project, pk=pk)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = self.project
            task.save()
            return redirect("tasks:list_project", kwargs={"pk": self.project.pk})
        return render(
            request, "tasks/create_task_view.html", {"form": form, "project_pk": pk}
        )

    def get(self, request, pk):
        form = TaskForm()
        return render(
            request, "tasks/create_task_view.html", {"form": form, "project_pk": pk}
        )


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update_task_view.html"
    pk_url_kwarg = "task_pk"
    context_object_name = "task"

    def form_valid(self, form):
        task = form.save()
        return redirect(reverse("tasks:list_task", kwargs={"pk": task.project.pk}))


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/delete_task_view.html"
    pk_url_kwarg = "task_pk"
    context_object_name = "task"

    def get_success_url(self, **kwargs):
        return reverse_lazy("tasks:list_task", kwargs={"pk": self.object.project.pk})


class TaskOverdueListView(ListView):
    model = Task
    template_name = "tasks/overdue_tasks_view.html"
    context_object_name = "overdue_tasks"

    def get_queryset(self):
        tasks_not_completed = Task.objects.filter(
            project=self.kwargs.get("pk"), completed=False
        )
        overdue_tasks = []
        for task in tasks_not_completed:
            if self.is_task_overdue(task):
                overdue_tasks.append(task)
        return overdue_tasks

    def is_task_overdue(self, task):
        now = datetime.now(timezone.utc)
        if task.end:
            if (task.end.date() - now.date()).days < 0:
                return True
            else:
                return False
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        return context
