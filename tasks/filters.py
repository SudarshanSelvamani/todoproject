from typing import Text
from django.db.models import fields
import django_filters
from .models import Project, Task
from django import forms


class TaskFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(lookup_expr="icontains")
    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all())
    end = django_filters.DateFromToRangeFilter(
        "end",
        label=("overdue after"),
        widget=django_filters.widgets.RangeWidget(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Task
        fields = ["text", "end"]
