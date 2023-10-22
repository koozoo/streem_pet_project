from django.http import StreamingHttpResponse
from django.shortcuts import render
from video import services


# Create your views here.
def get_streaming_video(request, **slug):
    if slug.get('movie_slug', None) is not None:
        media_slug = slug['movie_slug']
        _type = 'movie'
    else:
        media_slug = slug['show_slug']
        _type = 'show'

    file, status_code, content_length, content_range = services.open_file(request, slug=media_slug, type_video=_type)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range

    return response


def detail_video(request):
    ...
