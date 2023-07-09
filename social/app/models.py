from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.ManyToManyField('User', blank=True, related_name='following')

class Post(models.Model):
    poster = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    posted_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    liked_by = models.ManyToManyField('User', blank=True, related_name='liked_posts')
