from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from video import services
from video.models import VideoForStreem


def get_streaming_video(request, **slug):
    print("get_streaming_video", slug)

    video = get_object_or_404(VideoForStreem, pk=slug.get('pk_video', 0))

    if video.type == 'm':
        media_slug = slug['movie_slug']
        video_id = slug['pk_video']
        _type = 'movie'
    else:
        media_slug = slug['shows_slug']
        video_id = slug['pk_video']
        _type = 'show'

    file, status_code, content_length, content_range = services.open_file(request,
                                                                          slug=media_slug,
                                                                          type_video=_type,
                                                                          video_id=video_id)

    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range

    return response
