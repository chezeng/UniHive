from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now
import os
import uuid

class User(AbstractUser):
    pass

def post_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('pictures', str(instance.poster.id), new_filename)


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





# class Task(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     completed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# class Publisher(models.Model):
#     name = models.CharField(max_length=30)
#     address = models.CharField(max_length=60)

#     def __str__(self):
#         return self.name

    
# class Person(models.Model):
#     name = models.CharField("Char field", max_length=50)

#     def __str__(self):
#         return self.name
    
# class Group(models.Model):
#     name = models.CharField('group', max_length=100)
#     members = models.ManyToManyField(Person, verbose_name=("members"), through='Membership')

#     def __str__(self):
#         return self.name

# # What is related_name and what is this used for?

# class Membership(models.Model):
#     person = models.ForeignKey(Person, verbose_name=(""), on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, verbose_name=(""), on_delete=models.CASCADE, related_name='book')
#     date_joined = models.DateField("Date joined", auto_now=False, auto_now_add=False)
#     invite_reason = models.CharField(max_length=50)
#     test = models.ForeignKey("app.Model", verbose_name=(""), on_delete=models.SET_DEFAULT)
    
#     def get_absolute_url(self):
#         return reverse("blog:article_detail", kwargs={"pk": self.pk})
    
#     def viewed(self):
#         self.views += 1
#         self.save(update_fields=['views'])

# class EdwardBookManager(models.Manager):
#     def get_queryset(self) -> models.QuerySet:
#         return super().get_queryset().filter(author='Edward')
    


# class Book(models.Model):
#     name = models.CharField(max_length=30)
#     description = models.TextField(blank=True, null=True)
#     publisher = models.ForeignKey("publisher.model", verbose_name="Publisher", on_delete=models.CASCADE)
#     add_date = models.DateField(("Hello"), auto_now=False, auto_now_add=False)

#     objects = models.Manager() # The default manager
#     edward_objects = EdwardBookManager() # The Edward-specific manager

#     def __str__(self):
#         return self.name
    

# # --- This is an advanced model example --- 


# class HighRatingManager(models.Manager):
#     def get_queryset(self) -> models.QuerySet:
#         return super().get_queryset()


# class Rating(models.IntegerChoices):
#     EXCELLENT = 1, "Excellent"
#     GOOD = 2, 'Good'
#     MEDIUM = 3, 'Medium'


# class Product(models.Model):
#     # Database lists
#     name = models.CharField(_("name"), max_length=50)
#     rating = models.IntegerField(_("integer rating"), max_length=1, choices=Rating.choices)

#     # Managers
#     objects = models.Manager()
#     high_rating_products = HighRatingManager()
    
#     class Meta:
#         verbose_name = 'product'
#         verbose_name_plural = 'products'
    
#     def __str__(self):
#         return self.name
    
#     def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: os.Iterable[str] | None = ...) -> None:
#         return super().save(force_insert, force_update, using, update_fields)
    
#     def get_absolute_url(self):
#         return reverse("product_details", kwargs={"pk": self.pk})


# class Article(models.Model):
#     title = models.CharField(_("Title"), max_length=200, unique=True)
#     body = models.TextField(_("Content"))
#     created_at = models.DateTimeField(_("Date and time"), auto_now=False, auto_now_add=True)

#     def __str__(self):
#         return self.name


# # Save

# article_01 = Article(title='My first article', body='Well this is a body paragraph')
# article_01.save()


# # Delete

# Article.objects.get(pk=5).delete() # Delete the fifth article


# # Change 

# article_02 = Article.objects.get(id=1)
# article_02.title = 'New article title'
# article_02.save()


# # Check

# Article.objects.all()
# Article.objects.all().values() # Only for the values
# Article.objects.all().values('title') # Only for the values with 'title'

# article_03 = Article.objects.get(id=11) # Check the article with the id of 11

# # How does URLconf work?

