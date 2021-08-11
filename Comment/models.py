from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from CafeApp.models import Cafe


class Comment(models.Model):
    post = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    create_at = models.DateTimeField(default=timezone.now)