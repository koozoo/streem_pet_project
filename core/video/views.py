from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from video import services
from video.models import VideoForStreem


def get_streaming_video(request, **slug):
    # TODO revers on this method for streem
    video = get_object_or_404(VideoForStreem, pk=slug.get('pk_video', 0))

    if video.type == 'm':
        media_slug = slug['movie_slug']
        video_id = slug['pk_video']
        _type = 'movie'
    else:
        media_slug = slug['shows_slug']
        video_id = slug['pk_video']
        _type = 'show'
