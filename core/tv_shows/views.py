from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.db.models import F

from home.utils import MainPagesMixin
from services.media_mixin import MediaMixin
from tv_shows.models import Shows, ShowsItem
from tv_shows.utils import ShowsBuilder
from video.models import VideoForStreem


class MainShows(MainPagesMixin, TemplateView):
    template_name = 'tv_shows/tv-shows-home.html'
    title = 'Сериалы'
    dispatch_ = ShowsBuilder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DetailShows(TemplateView):
    template_name = 'tv_shows/single-tv-shows.html'

    seasons: dict = None
    total_video: int = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data, video = self._get_data_page(slug=kwargs['shows_slug'])
        self._videos(videos=video)

        context['title'] = "Сериалы",
        context['data'] = data,
        context['video_seasons'] = self.seasons,
        context['total_video'] = self.total_video,
        context['total_seasons'] = [i + 1 for i in range(data.seasons)],
        context['genre'] = [{"pk": genre.pk, "title": genre.title.capitalize(), "slug": genre.slug} for genre in data.genre.all()]

        self._update_counter(slug=kwargs['shows_slug'])

        return context

    def _get_data_page(self, slug):
        data = get_object_or_404(Shows.objects.filter(status='p', slug=slug))
        videos = ShowsItem.objects.filter(shows_id=data.pk, status='p')

        return data, videos

    def _videos(self, videos):
        self.seasons = {}
        self.total_video = 0

        for video in videos:
            if str(video.season) in self.seasons:
                self.seasons[f'{video.season}'] += [video]
            else:
                self.seasons[f'{video.season}'] = [video]

            self.total_video += 1

    def _update_counter(self, slug):
        views_counter = Shows.objects.get(status='p', slug=slug)
        views_counter.total_watch = F('total_watch') + 1
        views_counter.save()


class SingleEpisode(MediaMixin):
    template_name = 'tv_shows/single-tv-shows.html'
    type = 'shows'
    _CACHE_EXPIRE_TIME = 60

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self._update_view()

        return context

    def _build_context(self, slug):

        cache_item_name = f'media_cache_slug:{slug}'
        media_cache = cache.get(cache_item_name)

        if media_cache:
            data = media_cache
        else:
            data = get_object_or_404(Shows.objects.filter(status='p', slug=slug))
            cache.set(cache_item_name, data, self._CACHE_EXPIRE_TIME)

        videos = ShowsItem.objects.filter(shows_id=data.pk, status='p')

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

    def _update_view(self):
        # UPDATE BLOCK
        views_counter = Shows.objects.get(status='p', slug=shows_slug)
        views_counter.total_watch = F('total_watch') + 1
        views_counter.save()


def single_shows(request, shows_slug: str):
    # UPDATE BLOCK
    views_counter = Shows.objects.get(status='p', slug=shows_slug)
    views_counter.total_watch = F('total_watch') + 1
    views_counter.save()

    # DATA BLOCK
    data = get_object_or_404(Shows.objects.filter(status='p', slug=shows_slug))
    videos = ShowsItem.objects.filter(shows_id=data.pk, status='p')

    # SERVICE BLOCK
    seasons = {}
    total_video = 0

    for video in videos:
        if str(video.season) in seasons:
            seasons[f'{video.season}'] += [video]
        else:
            seasons[f'{video.season}'] = [video]

        total_video += 1

    context = {
        'title': "Сериалы",
        'data': data,
        'video_seasons': seasons,
        'total_video': total_video,
        'total_seasons': [i + 1 for i in range(data.seasons)],
        'genre': [{"pk": genre.pk, "title": genre.title.capitalize(), "slug": genre.slug} for genre in data.genre.all()]

    }

    return render(request, 'tv_shows/single-tv-shows.html', context=context)


def watch_series(request, shows_slug, season, pk_series):

    shows_info = get_object_or_404(Shows, slug=shows_slug)
    shows_item = get_object_or_404(ShowsItem, pk=pk_series)

    shows_videos = VideoForStreem.objects.filter(origin_video=pk_series)
    streem_items = {int(item.resolution): item for item in shows_videos}

    if shows_videos:
        context = {
            'data': shows_info,
            'shows_item': shows_item,
            'streem_items': streem_items,
            'title': 'Сериалы'
        }

        return render(request, 'tv_shows/single-episode.html', context=context)
    else:
        return render(request, 'tv_shows/tv-shows-home.html')
