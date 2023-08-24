from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, UpdateView
from django.db.models import Avg, FloatField, Case, When, Value

from w2w_app.filters import PersonFilter, MovieFilter
from w2w_app.forms import AddPersonModelForm, AddMovieModelForm, RatingCommentsForm, AddPlatformModelForm, \
    AddGenreModelForm
from w2w_app.models import Person, Movie, RatingComment, Genre, Platform
from what_to_watch.context_processors import user_is_moderator


# Create your views here.
class HomeView(View):
    def get(self, request):
        recently_added_movies = Movie.objects.order_by('-id')[:3]

        context = {
            'recently_added_movies': recently_added_movies
        }
        return render(request, 'home.html', context)


class PersonView(View):
    def get(self, request, person_id):
        person = Person.objects.get(pk=person_id)
        if person is not None:
            return render(request, 'person.html', {'person': person})
        else:
            raise Http404('Person does not exist')


class PersonsFilterFormView(View):

    def get(self, request):
        person_filter = PersonFilter(request.GET, queryset=Person.objects.all())
        context = {
            'form': person_filter.form,
            'object_list': person_filter.qs
        }
        return render(request, 'persons_list.html', context)


class AddPersonModelFormView(UserPassesTestMixin, View):

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
    model = Person
    fields = '__all__'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('update_person', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return user_is_moderator(self.request.user)


class AddMovieModelFormView(UserPassesTestMixin, View):

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

    def get(self, request):
        movie_filter = MovieFilter(request.GET, queryset=Movie.objects.all())
        context = {
            'form': movie_filter.form,
            'movies': movie_filter.qs
        }
        return render(request, 'movie_list.html', context)


class MovieView(View):
    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        if movie is not None:
            return render(request, 'movie.html', {'movie': movie})
        else:
            raise Http404('Movie does not exist')


class UpdateMovie(UserPassesTestMixin, UpdateView):
    model = Movie
    fields = '__all__'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('update_movie', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return user_is_moderator(self.request.user)


class RatingCommentsView(LoginRequiredMixin, View):

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

    def get(self, request):
        platforms = Platform.objects.all()
        return render(request, 'list_view.html', {'objects': platforms})


class UpdatePlatform(UserPassesTestMixin, UpdateView):
    model = Platform
    fields = '__all__'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('update_platform', kwargs={'pk': self.kwargs['pk']})


    def test_func(self):
        return user_is_moderator(self.request.user)



class AddGenreModelFormView(UserPassesTestMixin, View):

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

    def get(self, request):
        genres = Genre.objects.all()
        return render(request, 'list_view.html', {'objects': genres})


class UpdateGenre(UserPassesTestMixin, UpdateView):
    model = Genre
    fields = '__all__'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('update_genre', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return user_is_moderator(self.request.user)