from pathlib import Path

from django.shortcuts import get_object_or_404

from movie.models import Movie
from tv_shows.models import Shows


def open_file(request, video_pk: int, type_video: str = 'movie'):

    if type_video == "movie":
        _video = get_object_or_404(Movie, pk=video_pk)
    else:
        _video = get_object_or_404(Shows, pk=video_pk)

    path = Path(_video.path.path)

    file = path.open('rb')
    file_size = path.stat().st_size

    print(file)
    print(file_size)
