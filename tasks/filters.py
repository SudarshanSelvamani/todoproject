import django_filters
from .models import Project, Task


class TaskFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(lookup_expr="icontains")
    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = {"end": ["date__lte"]}
