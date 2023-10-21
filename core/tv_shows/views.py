from django.shortcuts import render, get_object_or_404

from tv_shows.models import Shows


# Create your views here.
def main_shows(request):
    context = {}
    return render(request, 'tv_shows/tv-shows-home.html')


def single_shows(request, shows_slug: str):
    data = get_object_or_404(Shows.objects.filter(status='p', slug=shows_slug))
    print(data.video)
    context = {
        'data': data
    }
    print(shows_slug)

    return render(request, 'movie/single-movie.html', context=context)
