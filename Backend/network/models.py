from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked")
    found = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='pictures/', blank=True, null=True)
    latitude = models.FloatField(default=43.4722893)
    longitude = models.FloatField(default=-80.5474325)  
    pinned = models.BooleanField(default=False)

class Network(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name="following")