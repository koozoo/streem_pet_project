from django.shortcuts import render, get_object_or_404
from movie.models import Movie
from video.models import Categories, Actors
from home import utils


# Create your views here.
def index(request):
    # init page builder
    home_page_builder = utils.HomePageBuilder(request=request, page_title='home')

    # get home page data
    context = home_page_builder.build()

    return render(request, 'home/index.html', context)
