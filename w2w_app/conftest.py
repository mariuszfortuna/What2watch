import pytest
from django.contrib.auth.models import User
from w2w_app.models import Person, Platform, Genre, Movie, RatingComment


@pytest.fixture
def persons():
    lst = []
    for x in range(10):
        p = Person.objects.create(first_name=x, last_name=x, photo='default_person.jpeg')
        lst.append(p)
    return lst


@pytest.fixture
def genres():
    lst = []
    for x in range(5):
        lst.append(Genre.objects.create(name='x'))
    return lst

@pytest.fixture
def platforms():
    lst = []
    for x in range(5):
        lst.append(Platform.objects.create(name='x', logo='default_logo.jpeg', website_link='x'))
    return lst




@pytest.fixture
def movies(persons, genres, platforms):
    lst = []
    for x in range(5):
        m = Movie()
        m.title = 'x'
        m.director = persons[x]
        m.platform = platforms[x]
        m.poster = 'default_movie.jpg'
        m.save()
        m.genres.set(genres)
        m.actors.set(persons)
        lst.append(m)
    return lst


