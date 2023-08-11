from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import Coalesce
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='person', default='default_person.jpeg')


class Platform(models.Model):
    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='logo')


class Genre(models.Model):
    name = models.CharField(max_length=128)


class Movie(models.Model):
    title = models.CharField(max_length=128)
    director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='directed_by')
    actors = models.ManyToManyField(Person, blank=True, related_name='cast')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    poster = models.ImageField(upload_to='covers', default='default_movie.jpg')

    def rating_avg(self):
        return RatingComment.objects.filter(movie=self).aggregate(
            avg=Coalesce(models.Avg('rating'), 0),
        )['avg']


class RatingComment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()
