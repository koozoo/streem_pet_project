from pathlib import Path

from django.shortcuts import render, get_object_or_404

from tv_shows.models import Shows, ShowsItem
from video.services import ConvertVideo
from video.models import Video, VideoForStreem

from video.services import VideoStreemData


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
    streem_items = {item.resolution: item.pk for item in shows_videos}

    if shows_videos:
        context = {
            'data': shows_info,
            'shows_item': shows_item,
            'streem_items': streem_items
        }
        print(context)
        return render(request, 'tv_shows/single-episode.html', context=context)
    else:
        return render(request, 'tv_shows/tv-shows-home.html')
