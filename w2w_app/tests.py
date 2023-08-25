import pytest
from django.test import Client
# Create your tests here.
from django.urls import reverse
from w2w_app.forms import AddMovieModelForm, AddPersonModelForm, AddPlatformModelForm
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
    assert response.context['person'] == person
    assert person.last_name in response.content.decode('utf-8')


@pytest.mark.django_db
def test_add_person_not_login():
    url = reverse('add_person')
    client = Client()
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_person_moderator_login(moderator):
    url = reverse('add_person')
    client = Client()
    client.force_login(moderator)
    response = client.get(url)
    assert response.status_code == 200
    dane = {'first_name': 'Jan',
            'last_name': 'Kowalski',
            }
    response = client.post(url, dane)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_movie_not_login():
    url = reverse('add_movie')
    client = Client()
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_movie_moderator_login(moderator, person, genres, platform, movie):
    url = reverse('add_movie')
    client = Client()
    client.force_login(moderator)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddMovieModelForm)
    dane = {'title': 'Tytul',
            'director': person.id,
            'actors': person.id,
            'platform': platform.id,
            'genres': [x.id for x in genres]
            }
    response = client.post(url, dane)
    assert response.status_code == 302


@pytest.mark.django_db
def test_movie_detail(movie):
    url = reverse('movie_detail', kwargs={'movie_id': movie.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['movie'] == movie


@pytest.mark.django_db
def test_update_movie_not_login(movie):
    url = reverse('update_movie', kwargs={'pk': movie.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_movie_moderator_login(movie, moderator):
    url = reverse('update_movie', kwargs={'pk': movie.id})
    client = Client()
    client.force_login(moderator)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['movie'] == movie

@pytest.mark.django_db
def test_update_person_not_login(person):
    url = reverse('update_person', kwargs={'pk': person.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_person_moderator_login(person, moderator):
    url = reverse('update_person', kwargs={'pk': person.id})
    client = Client()
    client.force_login(moderator)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['person'] == person


@pytest.mark.django_db
def test_add_platform_not_login():
    url = reverse('add_platform')
    client = Client()
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_platform_moderator_login(moderator):
    url = reverse('add_platform')
    client = Client()
    client.force_login(moderator)
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddPlatformModelForm)


@pytest.mark.django_db
def test_add_genre_not_login():
    url = reverse('add_genre')
    client = Client()
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_genre_moderator_login(moderator):
    url = reverse('add_genre')
    client = Client()
    client.force_login(moderator)
    response = client.get(url)
    assert response.status_code == 200
    dane = {'name': 'Komedia'}
    response = client.post(url, dane)
    assert response.status_code == 302


@pytest.mark.django_db
def test_genre_list_view(genres):
    url = reverse('genre_list')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['objects'].count() == len(genres)
    for genre in genres:
        assert genre in response.context['objects']


@pytest.mark.django_db
def test_platform_list_view(platforms):
    url = reverse('platform_list')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['objects'].count() == len(platforms)
    for platform in platforms:
        assert platform in response.context['objects']


@pytest.mark.django_db
def test_update_platform_not_login(platform):
    url = reverse('update_platform', kwargs={'pk': platform.id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_platform_moderator_login(platform, moderator):
    url = reverse('update_platform', kwargs={'pk': platform.id})
    client = Client()
    client.force_login(moderator)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['platform'] == platform


@pytest.mark.django_db
def test_update_genre_not_login(genres):
    url = reverse('update_genre', kwargs={'pk': genres[0].id})
    client = Client()
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_genre_moderator_login(genres, moderator):
    url = reverse('update_genre', kwargs={'pk': genres[0].id})
    client = Client()
    client.force_login(moderator)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['genre'] == genres[0]

