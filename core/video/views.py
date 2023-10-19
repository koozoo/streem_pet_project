from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request=request, template_name='video/index.html')


def main_show(request):
    return render(request=request, template_name='video/tv-shows-home.html')


def main_movie(request):
    return render(request=request, template_name='video/tv-shows-home.html')


def show_video(request):
    ...


def detail_video(request):
    ...
