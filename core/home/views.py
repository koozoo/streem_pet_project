from django.shortcuts import render, get_object_or_404
from movie.models import Movie
from video.models import Categories, Actors


# Create your views here.
def index(request):

    banner_videos = Movie.objects.filter(status='p')
    top_10 = Movie.objects.filter(status='p')

    context = {'banner_videos': banner_videos,
               'top_10': top_10}
    return render(request, 'home/index.html', context)
