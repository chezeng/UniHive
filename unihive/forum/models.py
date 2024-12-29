from django.db import models
from django.contrib.auth.models import AbstractUser
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=post_picture_path)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked')
    pinned = models.BooleanField(default=False)

    def __str__(self):
        return super().__str__()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name="following")
    liked = models.ManyToManyField(User, blank=True, related_name="likes")
    
    def __str__(self):
        return super().__str__()


class Message(models.Model):
    text = models.TextField()
    time = models.DateTimeField(default=now)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_message")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_message")
    
    def __str__(self):
        return super().__str__()




class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
