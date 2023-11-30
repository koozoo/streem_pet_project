from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.core.cache import cache

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
    _CACHE_EXPIRE_TIME = 60

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = context.get('movie_slug', None)

        data, movie_video, streem_items = self._build_context(slug=slug)

        context['data'] = data
        context['streem_items'] = streem_items
        context['title'] = f'Фильм - {data.title.capitalize()}'
        context['movie_video'] = movie_video

        self._update_counter(slug=slug)
        return context

    def _update_counter(self, slug):
        if slug is not None:
            views_counter = Movie.objects.get(status='p', slug=slug)
            views_counter.total_watch = F('total_watch') + 1
            views_counter.save()

    def _build_context(self, slug):
        cache_item_name = f'media_cache_slug:{slug}'
        media_cache = cache.get(cache_item_name)

        if media_cache:
            data = media_cache
        else:
            data = get_object_or_404(Movie.objects.filter(status='p', slug=slug))
            cache.set(cache_item_name, data, self._CACHE_EXPIRE_TIME)

        if data:
            video_cache_name = cache_item_name + ':video'
            streem_cache_name = cache_item_name + ':streem'

            video_cache = cache.get(video_cache_name)
            if video_cache:
                movie_video = video_cache
            else:
                movie_video = VideoForStreem.objects.filter(origin_video=data.video)
                cache.set(video_cache_name, movie_video, self._CACHE_EXPIRE_TIME)

            streem_cache = cache.get(streem_cache_name)
            if streem_cache:
                streem_items = streem_cache
            else:
                streem_items = {int(item.resolution): item for item in movie_video}
                cache.set(streem_cache_name, streem_items, self._CACHE_EXPIRE_TIME)

            return data, movie_video, streem_items


def single_movie(request, movie_slug):
    print('single movie ....')
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
