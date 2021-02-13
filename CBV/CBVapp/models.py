from django.db import models
from django.urls import reverse


class School(models.Model):
    name = models.CharField(max_length=150)
    principal = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('CBV:list')


class Student(models.Model):
    school = models.ForeignKey(
        School, related_name="students", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name
