from django.shortcuts import render
from video import services


# Create your views here.
def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = services.open_file(request, video_pk=pk)


def detail_video(request):
    ...
