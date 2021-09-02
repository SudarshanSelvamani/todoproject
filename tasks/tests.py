import random
from django.test import TestCase
from django.utils.timezone import now
from django.http import response
from django.urls import reverse, resolve
from datetime import timedelta
from tasks.models import Task, Project
from .forms import ProjectForm, TaskForm
from django.contrib.auth.models import User
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
    TaskFilterView,
)

# Create your tests here.
class Mixin:
    def create_project(
        self,
        project_name="Deployment",
    ):
        project = Project.objects.create(name=project_name)
        return project

    def create_task(self, task_text, project, end, assign_to=None, completed=False):
        task = Task.objects.create(
            text=task_text,
            project=project,
            assign_to=assign_to,
            end=end,
            completed=completed,
        )
        return task

    def create_user(self, username="johndoe", email="john@doe.com", password="1234"):
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return user


class FormTest(TestCase):
    def test_projectform_inputs(self):
        self.form_data = {"name": "to do app"}
        self.form = ProjectForm(data=self.form_data)
        self.assertTrue(self.form.is_valid())

    def test_taskform_inputs(self):
        self.form_data = {"text": "to do app"}
        self.form = TaskForm(data=self.form_data)
        self.assertTrue(self.form.is_valid())


class TestProjectListView(TestCase, Mixin):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

        user = self.create_user()
        self.client.force_login(user)

    def test_page_serve_successful(self):
        self.url = reverse("tasks:list_projects")
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_urls_resolve_project_list_object(self):
        view = resolve("/projects/")
        self.assertEquals(view.func.view_class, ProjectList)


class TestTaskListView(TestCase, Mixin):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )
        user = self.create_user()
        self.client.force_login(user)

    def test_page_serve_successful(self):
        self.url = reverse("tasks:list_task", args=[self.project1.pk])
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_task_list_object(self):
        view = resolve("/projects/1")
        self.assertEquals(view.func.view_class, TaskListView)


class TestProjectCreateView(TestCase, Mixin):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )
        user = self.create_user()
        self.client.force_login(user)

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


class TestProjectUpdateView(TestCase, Mixin):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )
        user = self.create_user()
        self.client.force_login(user)

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


class TestProjectDeleteView(TestCase, Mixin):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )
        user = self.create_user()
        self.client.force_login(user)

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


class TestTaskCreateView(TestCase, Mixin):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )
        user = self.create_user()
        self.client.force_login(user)

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


class TestTaskUpdateView(TestCase, Mixin):
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
        user = self.create_user()
        self.client.force_login(user)

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


class TestTaskDeleteView(TestCase, Mixin):
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
        user = self.create_user()
        self.client.force_login(user)

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


class TestTaskOverdueView(TestCase, Mixin):
    def setUp(self):
        self.user = self.create_user()
        self.client.force_login(self.user)

    def test_page_serve_successful(self):
        self.project1 = self.create_project(project_name="Deployment")
        self.url = reverse(
            "tasks:list_overdue_tasks",
            kwargs={"pk": self.project1.pk},
        )
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_overdue_task_list_object(self):
        view = resolve("/overduetasks/1")
        self.assertEquals(view.func.view_class, TaskOverdueListView)

    def test_response_contains_overdue_tasks(self):
        self.today = now()
        self.yesterday = self.today - timedelta(days=1)
        project1 = self.create_project(project_name="Deployment")
        project2 = self.create_project(project_name="Lollipop")
        task1 = self.create_task(
            task_text="test_overdue",
            project=project1,
            assign_to=self.user,
            end=self.yesterday,
        )

        task2 = self.create_task(
            task_text="test_overdue1",
            project=project2,
            assign_to=self.user,
            end=self.yesterday,
            completed=True,
        )

        url = reverse("tasks:list_overdue_tasks", args=[task1.project.pk])
        response = self.client.get(url)
        self.assertContains(response, task1)
        self.assertNotContains(response, task2)

    def test_response_contains_all_projects_overdue_tasks(self):
        self.today = now()
        self.yesterday = self.today - timedelta(days=1)
        project1 = self.create_project(project_name="Deployment")
        project2 = self.create_project(project_name="Lollipop")
        task1 = self.create_task(
            task_text="test_overdue",
            project=project1,
            assign_to=self.user,
            end=self.yesterday,
        )
        task2 = self.create_task(
            task_text="test_overdue1",
            project=project2,
            assign_to=self.user,
            end=self.yesterday,
        )
        url = reverse("tasks:list_all_overdue_tasks")
        response = self.client.get(url)
        self.assertContains(response, task1)
        self.assertContains(response, task2)


class TestTaskFilterView(TestCase, Mixin):
    def setUp(self):
        self.today = now()
        self.project1 = self.create_project(project_name="Search Task")
        self.task1 = self.create_task(
            task_text="search", project=self.project1, end=self.today
        )
        self.task2 = self.create_task(
            task_text="poppit", project=self.project1, end=self.today
        )
        user = self.create_user()
        self.client.force_login(user)

    def test_page_serve_successful(self):
        self.url = reverse("tasks:task_search")
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_task_filter_object(self):
        view = resolve("/taskssearch/")
        self.assertEquals(view.func.view_class, TaskFilterView)

    def test_presence_of_csrf(self):
        url = reverse("tasks:task_search")
        response = self.client.get(url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_search_results(self):
        self.client.post("/taskssearch/", {"text": "E"})
        url = reverse("tasks:task_search")
        response = self.client.get(url)
        self.assertContains(response, self.task1)
