import random
from django.test import TestCase
from django.http import response
from django.urls import reverse, resolve
from tasks.models import Task, Project
from .forms import ProjectForm
from .views import ProjectList

# Create your tests here.


class FormTest(TestCase):
    def test_projectform_inputs(self):
        self.form_data = {"name": "to do app"}
        self.form = ProjectForm(data=self.form_data)
        self.assertTrue(self.form.is_valid())

    def test_taskform_inputs(self):
        self.form_data = {"name": "to do app"}
        self.form = ProjectForm(data=self.form_data)
        self.assertTrue(self.form.is_valid())


class ModelTest(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

        self.project2 = Project.objects.create(name="Testing")

        self.task3 = Task.objects.create(
            text="Play", project=self.project2, completed=False
        )

        self.task4 = Task.objects.create(
            text="Sleep", project=self.project2, completed=False
        )

    def test_model_task(self):
        self.task5 = Task.objects.create(
            text="Analyze data", project=self.project1, completed=False
        )

        number_of_tasks_after_test_create = Task.objects.all().count()

        self.assertEquals(number_of_tasks_after_test_create, 5)

    def test_model_project(self):
        self.project3 = Project.objects.create(name="New features")

        number_of_projects_after_test_create = Project.objects.all().count()

        self.assertEquals(number_of_projects_after_test_create, 3)


class TestProjectListView(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="Deployment")

        self.task1 = Task.objects.create(
            text="Eat", project=self.project1, completed=True
        )

        self.task2 = Task.objects.create(
            text="Sleep", project=self.project1, completed=False
        )

        self.url = reverse("tasks:list_project")
        self.response = self.client.get(self.url)

    def test_page_serve_successful(self):
        self.assertEquals(self.response.status_code, 200)

    def test_project_list_object_is_served(self):
        view = resolve("/projects/")
        self.assertEquals(view.func.view_class, ProjectList)
