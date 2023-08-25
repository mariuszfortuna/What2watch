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
    assert response.context['movies'].count() == len(movies)
    for movie in movies:
        assert movie in response.context['movies']


@pytest.mark.django_db
def test_ratings_comments_for_movie(movies, user):
    url = reverse('ratings_comments_for_movie', kwargs={'movie_id': movies[0].id})
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    dane = {'rating': 5,
            'comment': 'komentarz'}
    response = client.post(url, dane)
    assert response.status_code == 302


@pytest.mark.django_db
def test_ratings_comments_for_movie_get_not_login(movie):
    url = reverse('ratings_comments_for_movie', kwargs={'movie_id': movie.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_person(person):
    url = reverse('person', kwargs={'person_id': person.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert str(person.first_name) in str(response.content)
    # Pobieranie kontekstu z odpowiedzi
    assert response.context['person'] == person

    # Sprawdzanie, czy imię osoby jest w którymkolwiek elemencie kontekstu
    # assert any(person.first_name in element for element in context)
    # assert person in context

    # Weryfikacja, czy imię i nazwisko osoby znajdują się w którymkolwiek elemencie kontekstu
    # assert person.first_name in response.content
    assert person.last_name in response.content.decode('utf-8')