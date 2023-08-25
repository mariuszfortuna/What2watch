from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView

from w2w_app.filters import PersonFilter, MovieFilter
from w2w_app.forms import AddPersonModelForm, AddMovieModelForm, RatingCommentsForm, AddPlatformModelForm, \
    AddGenreModelForm
from w2w_app.models import Person, Movie, RatingComment, Genre, Platform
from what_to_watch.context_processors import user_is_moderator


# Create your views here.

class HomeView(View):
    """HomeView class: Displays the home page with recently added movies."""

    def get(self, request):
        recently_added_movies = Movie.objects.order_by('-id')[:3]

        context = {
            'recently_added_movies': recently_added_movies
        }
        return render(request, 'home.html', context)


class PersonView(View):
    """PersonView class: Displays details about a specific person."""

    def get(self, request, person_id):
        person = Person.objects.get(pk=person_id)
        if person is not None:
            return render(request, 'person.html', {'person': person})
        else:
            raise Http404('Person does not exist')


class PersonsFilterFormView(View):
    """PersonsFilterFormView class: Displays a list of persons with filtering."""

    def get(self, request):
        person_filter = PersonFilter(request.GET, queryset=Person.objects.all())
        context = {
            'form': person_filter.form,
            'object_list': person_filter.qs
        }
        return render(request, 'persons_list.html', context)


class AddPersonModelFormView(UserPassesTestMixin, View):
    """AddPersonModelFormView class: Handles adding a new person."""

    def get(self, request):
        form = AddPersonModelForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddPersonModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('persons_list')
        return render(request, 'form.html', {'form': form})

    def test_func(self):
        return user_is_moderator(self.request.user)


class UpdatePerson(UserPassesTestMixin, UpdateView):
    """UpdatePerson class: Handles updating a person's details."""
    model = Person
    fields = '__all__'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('update_person', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return user_is_moderator(self.request.user)


class AddMovieModelFormView(UserPassesTestMixin, View):
    """AddMovieModelFormView class: Handles adding a new movie."""

    def get(self, request):
        form = AddMovieModelForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddMovieModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'form.html', {'form': form})

    def test_func(self):
        return user_is_moderator(self.request.user)


class MovieFilterFormView(View):
    """Displays a list of movies with filtering options.
    Handles the HTTP GET request and renders the filtered movie list."""

    def get(self, request):
        movie_filter = MovieFilter(request.GET, queryset=Movie.objects.all())
        context = {
            'form': movie_filter.form,
            'movies': movie_filter.qs
        }
        return render(request, 'movie_list.html', context)


class MovieView(View):
    """Detail movie view"""

    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        if movie is not None:
            return render(request, 'movie.html', {'movie': movie})
        else:
            raise Http404('Movie does not exist')


class UpdateMovie(UserPassesTestMixin, UpdateView):
    """Handles updating movie details."""
    model = Movie
    fields = '__all__'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('update_movie', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return user_is_moderator(self.request.user)


class RatingCommentsView(LoginRequiredMixin, View):
    """
       Handles viewing and adding rating comments for a movie.

       This view allows authenticated users to view and add comments and ratings for a movie.
       Users need to be logged in to access this view, as it inherits from LoginRequiredMixin.
    """

    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        ratings_comments = movie.ratings_comments.all()
        form = RatingCommentsForm()
        if movie is not None:
            return render(request, 'rating_comments_for_movie.html',
                          {'movie': movie, 'ratings_comments': ratings_comments, 'form': form})
        else:
            raise Http404('Movie does not exist')

    def post(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        ratings_comments = movie.ratings_comments.all()
        form = RatingCommentsForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            RatingComment.objects.create(movie=movie, user=request.user, rating=rating, comment=comment)
            return redirect('ratings_comments_for_movie', movie_id=movie_id)
        return render(request, 'rating_comments_for_movie.html',
                      {'movie': movie, 'ratings_comments': ratings_comments, 'form': form})


##

class AddPlatformModelFormView(UserPassesTestMixin, View):
    """
    Handles adding a new platform.

    This view allows authorized moderators to add a new platform to the system.
    It inherits from the UserPassesTestMixin and View.
    """

    def get(self, request):
        form = AddPlatformModelForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddPlatformModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'form.html', {'form': form})

    def test_func(self):
        return user_is_moderator(self.request.user)


class PlatformListView(View):
    """Displays a list of platforms."""

    def get(self, request):
        platforms = Platform.objects.all()
        return render(request, 'list_view.html', {'objects': platforms})


class UpdatePlatform(UserPassesTestMixin, UpdateView):
    """
      Handles updating platform details.

      This view allows authorized moderators to update the details of a platform.
      It inherits from the UserPassesTestMixin and UpdateView.
    """
    model = Platform
    fields = '__all__'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('update_platform', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return user_is_moderator(self.request.user)


class AddGenreModelFormView(UserPassesTestMixin, View):
    """Handles adding a new genre."""

    def get(self, request):
        form = AddGenreModelForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddGenreModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'form.html', {'form': form})

    def test_func(self):
        return user_is_moderator(self.request.user)


class GenreListView(View):
    """Displays a list of genres"""

    def get(self, request):
        genres = Genre.objects.all()
        return render(request, 'list_view.html', {'objects': genres})


class UpdateGenre(UserPassesTestMixin, UpdateView):
    """Handles updating genre details."""
    model = Genre
    fields = '__all__'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('update_genre', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return user_is_moderator(self.request.user)
