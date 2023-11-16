from django.views.generic import ListView
from genre.models import Genre
from django.core.paginator import Paginator
from django.shortcuts import render

from movie.models import Movie
from tv_shows.models import Shows


# class MainGenre(ListView):
#     template_name = 'home/base-collections.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         media = self._get_data(slug=context['genre_slug'])
#
#         context['collection_title'] = f"{context['genre_slug']}"
#         context['data'] = media
#         return context
#
#     def _get_data(self, slug):
#         genre_data = Genre.objects.filter(status='p', slug=slug)[0]
#
#         genre_media = []
#         [genre_media.append(item) for item in Movie.objects.filter(status='p', genre=genre_data)]
#         [genre_media.append(item) for item in Shows.objects.filter(status='p', genre=genre_data)]
#
#         return genre_media


def listing(request, genre_slug):
    limit = 20

    movie_list = [{"type": 'movie',
                   "genres": [{"slug": i.slug, "title": i.title} for i in item.genre.all()],
                   'entity': item} for item in Movie.objects.all()]
    shows_list = [{"type": 'movie',
                   "genres": [{"slug": i.slug, "title": i.title} for i in item.genre.all()],
                   'entity': item} for item in Shows.objects.all()]

    media_list = movie_list + shows_list
    paginator = Paginator(media_list, limit)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj,
               "collection_title": genre_slug}

    return render(request, 'home/base-collections.html', context)
