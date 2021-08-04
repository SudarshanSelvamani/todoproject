import random
from django.test import TestCase
from django.http import response
from django.urls import reverse, resolve
from tasks.models import Task, Project
from .forms import ProjectForm, TaskForm
from .views import ProjectList

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
