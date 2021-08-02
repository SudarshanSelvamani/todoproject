from django.db import models
from model_utils.models import TimeFramedModel
from taggit.managers import TaggableManager


# Create your models here


class Project(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Task(TimeFramedModel):
    text = models.CharField(max_length=40)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = TaggableManager()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="created_by"
    )
    assign_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="assigned_to",
    )
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text
