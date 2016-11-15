from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField


class Teacher(models.Model):
    name = models.CharField(max_length=10)
    photo_path = models.CharField(max_length=100)
    school = models.CharField(max_length=20)
    career = FroalaField(options={
        'width': 800,
        'height': 300,
    })
    sort = models.IntegerField()

    def _get_vote(self):
        return Vote.objects.filter(teacher_id=self.id).count()
    vote = property(_get_vote)

    def __str__(self):
        return self.name


class Vote(models.Model):
    teacher = models.ForeignKey(Teacher, related_name="voted")
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)


class Student(models.Model):
    sid = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
