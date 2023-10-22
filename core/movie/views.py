from django.shortcuts import render, get_object_or_404
from movie.models import Movie
from movie.utils import get_duration_video
from pathlib import Path


# Create your views here.
def main_movie(request):
    context = {}
    return render(request, 'movie/movies-home.html', context)


def single_movie(request, movie_slug):

    data = get_object_or_404(Movie.objects.filter(status='p', slug=movie_slug))

    context = {
        'data': data,
        'media_type': 'movie',
        'duration_video': get_duration_video(Path(data.video.path))
    }

    return render(request, 'movie/single-movie.html', context=context)
