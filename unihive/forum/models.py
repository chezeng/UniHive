from django.db import models

# Create your models here.

class Status(models.TextChoices):
    TODO = "t", "To do"
    IN_PROGRESS = "i", "In progress"
    COMPLETED = "c", "Completed"


class Task(models.Model):
    name = models.CharField(verbose_name="Task name", max_length=100, unique=True) 
    status = models.CharField(verbose_name="Task status", max_length=1, choices=Status.choices, default=Status.UNSTARTED)

    def __str__(self):
        return self.name
