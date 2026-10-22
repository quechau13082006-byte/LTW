from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100, help_text="The name of the project")
    description = models.TextField(help_text="The description of the project")
    def __str__(self):
        return self.name
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text="The title of the task")
    description = models.TextField(help_text="The description of the task")
    def __str__(self):
        return self.title
