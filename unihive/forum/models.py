from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import os
import uuid

# How does this function work?
def post_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('pictures/', new_filename)

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# # TODO: User properties to be refined
# class User():
#     username = models.TextField()


# class Post(models.Model):
#     picture = models.ImageField(upload_to=post_picture_path)
#     content = models.TextField()
#     time = models.DateTimeField(auto_now_add=True)
#     likes = models.ManyToManyField(User, blank=True, related_name='liked')
#     pinned = models.BooleanField(default=False)


# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     followers = models.ManyToManyField(User, blank=True, related_name="following")
#     liked = models.ManyToManyField(User, blank=True, related_name="Times to be liked")
    

# class Message(models.Model):
#     text = models.TextField()
#     time = models.DateTimeField(default=now)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_message")
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_message")
    

