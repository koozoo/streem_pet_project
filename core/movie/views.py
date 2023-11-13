from django.shortcuts import render, get_object_or_404
from movie.models import Movie
from pathlib import Path


# Create your views here.
def main_movie(request):
    context = {
        'title': 'Фильмы',
    }
    return render(request, 'movie/movies-home.html', context)


def single_movie(request, movie_slug):

    data = get_object_or_404(Movie.objects.filter(status='p', slug=movie_slug))

    context = {
        'data': data,
        'title': 'Фильмы',
        'media_type': 'movie',
        'duration_video': 0
    }

    return render(request, 'movie/single-movie.html', context=context)
