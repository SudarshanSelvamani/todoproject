import random
from django.test import TestCase
from django.http import response
from django.urls import reverse, resolve
from datetime import datetime, timezone, timedelta
from tasks.models import Task, Project
from .forms import ProjectForm, TaskForm
from .views import (
    ProjectList,
    TaskListView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskCreateView,
    ProjectCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskOverdueListView,
    AllTaskOverdueListView,
)

# Create your tests here.


class FormTest(TestCase):
    def test_projectform_inputs(self):
        self.form_data = {"name": "to do app"}
        self.form = ProjectForm(data=self.form_data)
        self.assertTrue(self.form.is_valid())

    def test_taskform_inputs(self):
        self.form_data = {"text": "to do app"}
        self.form = TaskForm(data=self.form_data)
        self.assertTrue(self.form.is_valid())


class TestProjectListView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

        self.url = reverse("tasks:list_projects")

    def test_page_serve_successful(self):
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_urls_resolve_project_list_object(self):
        view = resolve("/projects/")
        self.assertEquals(view.func.view_class, ProjectList)


class TestTaskListView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

    def test_page_serve_successful(self):
        self.url = reverse("tasks:list_task", args=[self.project1.pk])
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_task_list_object(self):
        view = resolve("/projects/1")
        self.assertEquals(view.func.view_class, TaskListView)


class TestProjectCreateView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

    def test_page_serve_successful(self):
        self.url = reverse("tasks:create_project")
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_project_update_object(self):
        view = resolve("/projects/create")
        self.assertEquals(view.func.view_class, ProjectCreateView)

    def test_presence_of_csrf(self):
        url = reverse("tasks:create_project")
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_response_contains_projectform_object(self):
        url = reverse("tasks:create_project")
        response = self.client.get(url)
        form = response.context.get("form")
        self.assertIsInstance(form, ProjectForm)

    def test_project_save(self):
        self.client.post("/projects/create", {"name": "I am a test project"})
        self.assertEqual(Project.objects.last().name, "I am a test project")


class TestProjectUpdateView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

    def test_page_serve_successful(self):
        self.url = reverse("tasks:update_project", kwargs={"pk": self.project1.pk})
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_project_update_object(self):
        view = resolve("/projects/1/update")
        self.assertEquals(view.func.view_class, ProjectUpdateView)

    def test_presence_of_csrf(self):
        url = reverse("tasks:update_project", args=[self.project1.pk])
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")


class TestProjectDeleteView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

    def test_page_serve_successful(self):
        self.url = reverse("tasks:delete_project", kwargs={"pk": self.project1.pk})
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_project_delete_object(self):
        view = resolve("/projects/1/delete")
        self.assertEquals(view.func.view_class, ProjectDeleteView)

    def test_presence_of_csrf(self):
        url = reverse("tasks:delete_project", args=[self.project1.pk])
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")


class TestTaskCreateView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

    def test_page_serve_successful(self):
        self.url = reverse("tasks:create_task", args=[self.project1.pk])
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_task_create_object(self):
        view = resolve("/projects/1/tasks/create")
        self.assertEquals(view.func.view_class, TaskCreateView)

    def test_presence_of_csrf(self):
        url = reverse("tasks:create_task", args=[self.project1.pk])
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_response_contains_taskform_object(self):
        url = reverse("tasks:create_task", args=[self.project1.pk])
        response = self.client.get(url)
        form = response.context.get("form")
        self.assertIsInstance(form, TaskForm)

    def test_task_saves(self):
        self.client.post(
            "/projects/1/tasks/create", {"text": "I am a test task", "completed": False}
        )
        self.assertEqual(Task.objects.last().project.name, self.project1.name)


class TestTaskUpdateView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

        self.url = reverse(
            "tasks:update_task",
            kwargs={"pk": self.project1.pk, "task_pk": self.task1.pk},
        )

    def test_page_serve_successful(self):
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_task_update_object(self):
        view = resolve("/projects/1/tasks/1/update")
        self.assertEquals(view.func.view_class, TaskUpdateView)

    def test_presence_of_csrf(self):
        url = reverse("tasks:update_task", args=[self.project1.pk, self.task1.pk])
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")


class TestTaskDeleteView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

        self.url = reverse(
            "tasks:delete_task",
            kwargs={"pk": self.project1.pk, "task_pk": self.task1.pk},
        )

    def test_page_serve_successful(self):
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_task_delete_object(self):
        view = resolve("/projects/1/tasks/1/delete")
        self.assertEquals(view.func.view_class, TaskDeleteView)

    def test_presence_of_csrf(self):
        url = reverse("tasks:delete_task", args=[self.project1.pk, self.task1.pk])
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")


class TestTaskOverdueView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

    def test_page_serve_successful(self):
        self.url = reverse(
            "tasks:list_overdue_tasks",
            kwargs={"pk": self.project1.pk},
        )
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_over_duetask_list_object(self):
        view = resolve("/projects/1/overduetasks")
        self.assertEquals(view.func.view_class, TaskOverdueListView)

    def test_overdue_tasks_(self):
        self.today = datetime.now(timezone.utc)
        self.yesterday = self.today - timedelta(days=1)
        self.task1 = Task.objects.create(
            text="Overduetesttask",
            project=self.project1,
            end=self.yesterday,
            completed=False,
        )
        url = reverse("tasks:list_overdue_tasks", args=[self.project1.pk])
        response = self.client.get(url)
        self.assertContains(response, self.task1)


class TestAllTasksOverdueView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Test Project 1")
        self.project2 = Project.objects.create(name="Test Project 2")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

    def test_page_serve_successful(self):
        self.url = reverse(
            "tasks:all_overdue_tasks",
        )
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_over_duetask_list_object(self):
        view = resolve("/")
        self.assertEquals(view.func.view_class, AllTaskOverdueListView)

    def test_overdue_tasks_(self):
        self.today = datetime.now(timezone.utc)
        self.yesterday = self.today - timedelta(days=1)
        self.task1 = Task.objects.create(
            text="Overduetesttask in project 1",
            project=self.project1,
            end=self.yesterday,
            completed=False,
        )
        self.task2 = Task.objects.create(
            text="Overduetesttask in project 2",
            project=self.project2,
            end=self.yesterday,
            completed=False,
        )
        url = reverse("tasks:all_overdue_tasks")
        response = self.client.get(url)
        self.assertContains(response, self.task1)
        self.assertContains(response, self.task2)
