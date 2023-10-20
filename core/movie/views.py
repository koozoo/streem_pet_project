from django.shortcuts import render


# Create your views here.
def main_movie(request):
    context = {}
    return render(request, 'movie/movies-home.html', context)
