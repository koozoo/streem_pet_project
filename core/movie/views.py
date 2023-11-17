from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView

from home.utils import MainPagesMixin
from movie.models import Movie

from movie.utils import MovieBuilder
from video.models import VideoForStreem


class MainMovie(MainPagesMixin, TemplateView):
    template_name = 'movie/movies-home.html'
    title = 'Фильмы'
    dispatch_ = MovieBuilder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DetailMovie(TemplateView):
    template_name = 'movie/single-movie.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = context.get('movie_slug', None)
        self._update_counter(slug=slug)
        data, movie_video, streem_items = self._build_context(slug=slug)

        context['data'] = data
        context['streem_items'] = streem_items
        context['title'] = f'Фильм - {data.title.capitalize()}'
        context['movie_video'] = movie_video

        print(context)
        return context

    def _update_counter(self, slug):
        if slug is not None:
            views_counter = Movie.objects.get(status='p', slug=slug)
            views_counter.total_watch = F('total_watch') + 1
            views_counter.save()

    def _build_context(self, slug):
        data = get_object_or_404(Movie.objects.filter(status='p', slug=slug))

        if data:
            movie_video = VideoForStreem.objects.filter(origin_video=data.video)
            streem_items = {int(item.resolution): item for item in movie_video}

            return data, movie_video, streem_items


def single_movie(request, movie_slug):

    data = get_object_or_404(Movie.objects.filter(status='p', slug=movie_slug))

    movie_video = VideoForStreem.objects.filter(origin_video=data.video)
    streem_items = {int(item.resolution): item for item in movie_video}
    context = {
        'data': data,
        'title': 'Фильмы',
        'streem_items': streem_items
    }
    print(context)
    return render(request, 'movie/single-movie.html', context=context)
