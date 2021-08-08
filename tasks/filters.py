from django.db.models import fields
import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            "text": ["icontains"],
        }
