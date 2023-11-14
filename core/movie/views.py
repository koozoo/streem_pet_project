from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from home.utils import DataMixin
from movie.models import Movie

from movie.utils import MovieBuilder
from video.models import VideoForStreem


class MainMovie(DataMixin, TemplateView):
    template_name = 'movie/movies-home.html'
    title = 'Фильмы'
    dispatch_ = MovieBuilder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def single_movie(request, movie_slug):

    data = get_object_or_404(Movie.objects.filter(status='p', slug=movie_slug))

    shows_videos = VideoForStreem.objects.filter(origin_video=data.video)
    streem_items = {int(item.resolution): item for item in shows_videos}
    context = {
        'data': data,
        'title': 'Фильмы',
        'streem_items': streem_items
    }
    print(context)
    return render(request, 'movie/single-movie.html', context=context)
