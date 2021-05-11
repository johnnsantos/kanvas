from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Activity(models.Model):
    repo = models.CharField(max_length=255, unique=True)
    grade = models.IntegerField(default=None, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
