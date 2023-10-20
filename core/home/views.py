from django.shortcuts import render, get_object_or_404
from movie.models import Movie
from video.models import Categories, Actors


# Create your views here.
def index(request):
    query = Movie.objects.filter(status='p')
    item = get_object_or_404(query.all())
    context = {'test': item}
    return render(request, 'home/index.html', context)
