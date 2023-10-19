from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request=request, template_name='video/index.html')


def main_show(request):
    return ...


def main_movie(request):
    ...


def show_video(request):
    ...


def detail_video(request):
    ...
