from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


app_name = "tasks"

urlpatterns = [
    path("projects/", views.ProjectList.as_view(), name="create_and_list_project"),
]
