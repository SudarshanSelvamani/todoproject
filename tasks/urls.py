from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


app_name = "tasks"

urlpatterns = [
    path("projects/", views.ProjectList.as_view(), name="list_projects"),
    path("projects/<str:pk>", views.TaskListView.as_view(), name="list_task"),
    path(
        "projects/<str:pk>/update",
        views.ProjectUpdateView.as_view(),
        name="update_project",
    ),
    path(
        "projects/<str:pk>/delete",
        views.ProjectDeleteView.as_view(),
        name="delete_project",
    ),
    path(
        "projects/<str:pk>/tasks/create",
        views.TaskCreateView.as_view(),
        name="create_task",
    ),
]
