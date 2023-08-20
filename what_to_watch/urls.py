"""
URL configuration for what_to_watch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from w2w_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('person/<int:person_id>', views.PersonView.as_view(), name='person'),
    path('addPerson/', views.AddPersonModelFormView.as_view(), name='add_person'),
    path('persons/', views.PersonsGenericListView.as_view(), name='persons_list'),
    path('addMovie/', views.AddMovieModelFormView.as_view(), name='add_movie'),
    path('Movies/', views.MoviesListView.as_view(), name='movie_list'),
    path('movie/<int:movie_id>/', views.MovieView.as_view(), name='movie_detail'),
    path('movie/<int:movie_id>/ratings_comments/', views.RatingCommentsView.as_view(), name='ratings_comments_for_movie'),
    path('updateMovie/<int:pk>/', views.UpdateMovie.as_view(), name='update_movie'),
    path('updatePerson/<int:pk>/', views.UpdatePerson.as_view(), name='update_person'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


