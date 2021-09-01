import json
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import datetime, timezone
from .models import Project, Task
from .filters import TaskFilter
from django.urls.base import reverse_lazy, reverse
from .forms import TaskForm, ProjectForm
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.


@method_decorator(login_required, name="dispatch")
class ProjectList(ListView):
    template_name = "tasks/project_list_view.html"
    model = Project
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(permitted_users=self.request.user)


@method_decorator(login_required, name="dispatch")
class ProjectCreateView(View):
    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.permitted_users.add(self.request.user)

            return redirect("tasks:list_projects")
        return render(request, "tasks/create_project_view.html", {"form": form})

    def get(self, request):
        form = ProjectForm()
        return render(request, "tasks/create_project_view.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class ProjectUpdateView(
    UserPassesTestMixin,
    UpdateView,
):
    model = Project
    fields = ("name", "permitted_users")
    template_name = "tasks/edit_project_view.html"
    pk_url_kwarg = "pk"
    context_object_name = "project"

    def test_func(self):
        user = self.request.user
        return user.project_set.filter(pk=self.kwargs.get("pk")).exists()

    def form_valid(self, form):
        project = form.save()
        return redirect(
            "tasks:list_projects",
        )


@method_decorator(login_required, name="dispatch")
class ProjectDeleteView(UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("tasks:list_projects")
    template_name = "tasks/delete_project_view.html"
    pk_url_kwarg = "pk"
    context_object_name = "project"

    def test_func(self):
        user = self.request.user
        return user.project_set.filter(pk=self.kwargs.get("pk")).exists()


@method_decorator(login_required, name="dispatch")
class TaskListView(UserPassesTestMixin, ListView):
    template_name = "tasks/task_list_view.html"
    model = Task
    context_object_name = "tasks"

    def test_func(self):
        user = self.request.user
        return user.project_set.filter(pk=self.kwargs.get("pk")).exists()

    def get_queryset(self):
        return Task.objects.filter(
            project=self.kwargs.get("pk"), assign_to=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        context["task_assigned_to_others"] = Task.objects.filter(
            project=self.kwargs.get("pk"), created_by=self.request.user
        ).exclude(assign_to=self.request.user)
        return context


@method_decorator(login_required, name="dispatch")
class TaskCreateView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        return user.project_set.filter(pk=self.kwargs.get("pk")).exists()

    def post(self, request, pk):
        self.project = get_object_or_404(Project, pk=pk)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = self.project
            task.created_by = self.request.user
            if task.assign_to == None:
                task.assign_to = self.request.user
            task.save()
            return redirect(reverse("tasks:list_task", kwargs={"pk": self.project.pk}))
        return render(
            request, "tasks/create_task_view.html", {"form": form, "project_pk": pk}
        )

    def get(self, request, pk):
        form = TaskForm()
        return render(
            request, "tasks/create_task_view.html", {"form": form, "project_pk": pk}
        )


@method_decorator(login_required, name="dispatch")
class TaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update_task_view.html"
    pk_url_kwarg = "task_pk"
    context_object_name = "task"

    def test_func(self):
        user = self.request.user
        return user.project_set.filter(pk=self.kwargs.get("pk")).exists()

    def form_valid(self, form):
        task = form.save()
        return redirect(reverse("tasks:list_task", kwargs={"pk": task.project.pk}))


@login_required
def task_completed_view(request, pk, task_pk):
    if request.is_ajax():
        task = get_object_or_404(Task, pk=task_pk)
        task.completed = not task.completed
        task.save()
    return JsonResponse({"ok": True}, status=200)


@method_decorator(login_required, name="dispatch")
class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/delete_task_view.html"
    pk_url_kwarg = "task_pk"
    context_object_name = "task"

    def test_func(self):
        user = self.request.user
        return user.project_set.filter(pk=self.kwargs.get("pk")).exists()

    def get_success_url(self, **kwargs):
        return reverse_lazy("tasks:list_task", kwargs={"pk": self.object.project.pk})


@method_decorator(login_required, name="dispatch")
class TaskOverdueListView(ListView):
    model = Task
    template_name = "tasks/overdue_tasks_view.html"
    context_object_name = "overdue_tasks"

    def get_queryset(self):
        overdue_tasks = Task.objects.filter(
            assign_to=self.request.user,
            end__lte=now(),
            completed=False,
        )
        project = self.kwargs.get("pk", None)

        if project:
            overdue_tasks = overdue_tasks.filter(project=project)

        return overdue_tasks


@method_decorator(login_required, name="dispatch")
class TaskFilterView(ListView):
    model = Task
    template_name = "tasks/tasks_filter_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = TaskFilter(self.request.GET, queryset=self.get_queryset())
        return context
