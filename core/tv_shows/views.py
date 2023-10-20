from django.shortcuts import render


# Create your views here.
def main_shows(request):
    context = {}
    return render(request, 'tv_shows/tv-shows-home.html')
