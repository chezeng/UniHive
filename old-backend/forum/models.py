from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
import os
import uuid

class User(AbstractUser):
    pass

def post_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('pictures/', new_filename)

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked")
    found = models.BooleanField(default=False)
    picture = models.ImageField(upload_to=post_picture_path, blank=True, null=True)
    latitude = models.FloatField(default=43.4722893)
    longitude = models.FloatField(default=-80.5474325)  
    pinned = models.BooleanField(default=False)

class Network(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name="following")

class Message(models.Model):
    text = models.TextField()
    time = models.DateTimeField(default=now)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_message")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_message")