from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.db.models import F

from tv_shows.models import Shows, ShowsItem
from video.models import Video, VideoForStreem
from genre.models import Genre


class MainShows(TemplateView):
    template_name = 'tv_shows/tv-shows-home.html'


class SingleShows(TemplateView):
    template_name = 'tv_shows/single-tv-shows.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['data'] = data,
    #     context['video_seasons'] = seasons,
    #     context['total_video'] = total_video,
    #     context['total_seasons'] = [i + 1 for i in range(data.seasons)]

    def _get_block_data(self):
        # DATA BLOCK
        data = get_object_or_404(Shows.objects.filter(status='p', slug=shows_slug))
        videos = ShowsItem.objects.filter(shows_id=data.pk, status='p')
        print(data.genre)
        # genre = ', '.join(Genre.objects.filter(shows_id=data.pk, status='p')).rstrip(',')
        # print(genre)


def single_shows(request, shows_slug: str):
    # UPDATE BLOCK
    views_counter = Shows.objects.get(status='p', slug=shows_slug)
    views_counter.total_watch = F('total_watch') + 1
    views_counter.save()

    # DATA BLOCK
    data = get_object_or_404(Shows.objects.filter(status='p', slug=shows_slug))
    videos = ShowsItem.objects.filter(shows_id=data.pk, status='p')
    print(data.genre)
    # genre = ', '.join(Genre.objects.filter(shows_id=data.pk, status='p')).rstrip(',')
    # print(genre)

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
        'data': data,
        'video_seasons': seasons,
        'total_video': total_video,
        'total_seasons': [i + 1 for i in range(data.seasons)]
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
            'streem_items': streem_items
        }

        return render(request, 'tv_shows/single-episode.html', context=context)
    else:
        return render(request, 'tv_shows/tv-shows-home.html')
