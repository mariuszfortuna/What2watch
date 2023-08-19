from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.db.models import Avg, FloatField, Case, When, Value

from w2w_app.forms import AddPersonModelForm, AddMovieModelForm, RatingCommentsForm
from w2w_app.models import Person, Movie, RatingComment



# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, template_name='home.html')


class PersonView(View):
    def get(self, request, person_id):
        person = Person.objects.get(pk=person_id)
        if person is not None:
            return render(request, 'person.html', {'person': person})
        else:
            raise Http404('Person does not exist')


class AddPersonModelFormView(View):

    def get(self, request):
        form = AddPersonModelForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddPersonModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('persons_list')
        return render(request, 'form.html', {'form': form})


class PersonsGenericListView(ListView):
    model = Person
    template_name = 'persons_list.html'


class AddMovieModelFormView(View):

    def get(self, request):
        form = AddMovieModelForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddMovieModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'form.html', {'form': form})


class MoviesListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    context_object_name = 'movies'

    # queryset = Movie.objects.annotate(avg_rating=Avg('ratings_comments__rating')).order_by('-avg_rating')

    def get_queryset(self):
        queryset = Movie.objects.annotate(
            rating_avg=Avg('ratings_comments__rating'),
        ).annotate(
            has_ratings=Case(
                When(ratings_comments__isnull=True, then=Value(0)),
                default=Value(1),
                output_field=FloatField()
            )
        )
        return queryset.order_by('-has_ratings', '-rating_avg')


class MovieView(View):
    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        if movie is not None:
            return render(request, 'movie.html', {'movie': movie})
        else:
            raise Http404('Movie does not exist')


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
            # form.save()
            return redirect('ratings_comments_for_movie', movie_id=movie_id)
        return render(request, 'rating_comments_for_movie.html',
                      {'movie': movie, 'ratings_comments': ratings_comments, 'form': form})
