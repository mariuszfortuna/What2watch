import pytest
from django.test import Client
# Create your tests here.
from django.urls import reverse
from w2w_app.forms import AddMovieModelForm, AddPersonModelForm
from w2w_app.models import Person, Platform, Genre, Movie, RatingComment


@pytest.mark.django_db
def test_home():
    url = reverse('home')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_person_list_view(persons):
    url = reverse('persons_list')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == len(persons)
    for person in persons:
        assert person in response.context['object_list']


@pytest.mark.django_db
def test_movie_list_view(movies):
    browser = Client()
    url = reverse('movie_list')
    response = browser.get(url)
    assert response.status_code == 200

    for movie in movies:
        assert any(movie.title == listed_movie.title for listed_movie in response.context['movies'])
        assert any(movie.director == listed_movie.director for listed_movie in response.context['movies'])
        assert any(movie.platform == listed_movie.platform for listed_movie in response.context['movies'])
        assert any(movie.poster == listed_movie.poster for listed_movie in response.context['movies'])
        assert any(movie.genres == listed_movie.genres for listed_movie in response.context['movies'])
        assert any(movie.actors == listed_movie.actors for listed_movie in response.context['movies'])
