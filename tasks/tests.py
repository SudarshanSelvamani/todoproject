import random
from django.test import TestCase
from django.http import response
from django.urls import reverse, resolve
from tasks.models import Task, Project
from .forms import ProjectForm

# Create your tests here.


class FormTest(TestCase):
    def setUp(self):
        self.response = self.client.get(self.url)

    def test_projectform_inputs(self):
        self.form_data = {"name": "to do app"}
        self.form = ProjectForm(data=self.form_data)
        self.assertTrue(self.form.is_valid())

