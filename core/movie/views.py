from django.shortcuts import render, get_object_or_404
from movie.models import Movie


# Create your views here.
def main_movie(request):
    context = {}
    return render(request, 'movie/movies-home.html', context)


def single_movie(request, movie_slug):

    data = get_object_or_404(Movie.objects.filter(status='p', slug=movie_slug))
    print(data.video)
    context = {
        'data': data
    }
    print(movie_slug)

    return render(request, 'movie/single-movie.html', context=context)
