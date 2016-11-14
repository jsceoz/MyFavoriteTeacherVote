from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    name = models.CharField(max_length=10)
    photo_path = models.CharField(max_length=100)
    school = models.CharField(max_length=20)
    career = models.TextField()

    def __str__(self):
        return self.name


class Vote(models.Model):
    teacher = models.ForeignKey(Teacher, related_name="voted")
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
