from django import forms

from .models import Person, Platform, Movie, Genre, RatingComment


class AddPersonModelForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    photo = forms.ImageField(required=False)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'photo']


class AddMovieModelForm(forms.ModelForm):
    title = forms.CharField()
    director = forms.ModelChoiceField(queryset=Person.objects.all(), required=False)
    actors = forms.ModelMultipleChoiceField(queryset=Person.objects.all(), required=False)
    platform = forms.ModelChoiceField(queryset=Platform.objects.all())
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())
    poster = forms.ImageField(required=False)

    class Meta:
        model = Movie
        fields = ['title', 'director', 'actors', 'platform', 'genres', 'poster']


class RatingCommentsForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]  # Tworzy listę krotek (wartość, etykieta)
    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Rating')
    comment = forms.CharField(widget=forms.Textarea, label='Comment')

    class Meta:
        model = RatingComment
        fields = ['rating', 'comment']


class AddPlatformModelForm(forms.ModelForm):
    name = forms.CharField()
    logo = forms.ImageField()
    website_link = forms.URLField()

    class Meta:
        model = Platform
        fields = ['name', 'logo', 'website_link']


class AddGenreModelForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Genre
        fields = ['name']
