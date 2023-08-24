from django.contrib.auth.models import User
from django.db import models
from django.db.models import DecimalField
from django.db.models.functions import Coalesce
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='person', default='default_person.jpeg')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Platform(models.Model):
    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='logo')
    website_link = models.URLField(default='')

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse('update_platform', kwargs={'pk': self.id})


class Genre(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse('update_genre', kwargs={'pk': self.id})


class Movie(models.Model):
    title = models.CharField(max_length=128)
    director = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE, related_name='directed_by')
    actors = models.ManyToManyField(Person, blank=True, related_name='cast')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    poster = models.ImageField(upload_to='covers', default='default_movie.jpg')

    def rating_avg(self):
        return RatingComment.objects.filter(movie=self).aggregate(
            avg=Coalesce(models.Avg('rating'), 0, output_field=DecimalField()),
        )['avg']


class RatingComment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()
