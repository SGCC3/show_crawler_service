from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Show(models.Model):
    title = models.CharField(max_length=50)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    runningTime = models.IntegerField()
    actors = models.TextField()
    directors = models.TextField()
    likes = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.title


class Reviews(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    stars = models.IntegerField()

    def __str__(self):
        return self.title

