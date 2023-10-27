from django.shortcuts import render, get_object_or_404

from tv_shows.models import Shows, ShowsItem
from movie.utils import get_duration_video


def main_shows(request):
    context = {}
    return render(request, 'tv_shows/tv-shows-home.html')


def single_shows(request, shows_slug: str):
    data = get_object_or_404(Shows.objects.filter(status='p', slug=shows_slug))
    videos = ShowsItem.objects.filter(shows_id=data.pk, status='p')
    # genre = ', '.join(Genre.objects.filter(shows_id=data.pk, status='p')).rstrip(',')
    seasons = {}
    total_video = 0
    for video in videos:
        if str(video.season) in seasons:
            seasons[f'{video.season}'] += [video]
        else:
            seasons[f'{video.season}'] = [video]

        total_video += 1
    print('seasons', seasons)
    context = {
        'data': data,
        'video_seasons': seasons,
        'total_video': total_video,
        'total_seasons': [i + 1 for i in range(data.seasons)]
    }

    return render(request, 'tv_shows/single-tv-shows.html', context=context)


def watch_series(request, shows_slug, season, pk_series):
    shows_info = get_object_or_404(Shows, slug=shows_slug)
    print(shows_info)
    shows_item = get_object_or_404(ShowsItem, pk=pk_series)
    print('items', shows_item)
    context = {
        'data': shows_info,
        'video': shows_item
    }
    print(context)
    return render(request, 'tv_shows/single-episode.html', context=context)
