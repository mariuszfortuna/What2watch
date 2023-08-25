import django_filters

from w2w_app.models import Person, Movie


class PersonFilter(django_filters.FilterSet):
    """Filter configuration for Person List"""

    class Meta:
        model = Person
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
        }


class MovieFilter(django_filters.FilterSet):
    """Filter configuration for Movie List"""

    class Meta:
        model = Movie
        fields = {
            'title': ['icontains'],
            'director': ['exact'],

            'platform': ['exact'],
            'genres': ['exact']
        }
