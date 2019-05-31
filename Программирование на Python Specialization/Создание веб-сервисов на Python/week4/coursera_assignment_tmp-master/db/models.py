from django.utils import timezone

from django.db import models


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User)
    created = models.DateTimeField(default=timezone.now)

    subscribers = models.ManyToManyField(User, related_name='subscriptions')


class Topic(models.Model):
    title = models.CharField(max_length=255)
    blog = models.ForeignKey(Blog)
    author = models.ForeignKey(User)
    created = models.DateTimeField(default=timezone.now)

    likes = models.ManyToManyField(User, related_name='likes')
