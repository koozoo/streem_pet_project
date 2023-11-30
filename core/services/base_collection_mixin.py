from django.core.cache import cache
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from genre.models import Genre
from movie.models import Movie
from tags.models import Tags
from tv_shows.models import Shows


class BaseCollection(TemplateView):
    template_name = 'home/base-collections.html'
    media_collection: list = None
    limit: int = None
    type: str = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_name = 'cache'

        if self.type == 'genre':
            cache_genre = cache.get(cache_name + ':genre')
            if cache_genre:
                collection_entity = cache_genre
            else:
                collection_entity = Genre.objects.filter(status='p', slug=context.get('genre_slug'))
                cache.set(cache_name + ':genre', collection_entity, 60)
        else:
            cache_tags = cache.get(cache_name + ':tags')
            if cache_tags:
                collection_entity = cache_tags
            else:
                collection_entity = Tags.objects.filter(status='p', slug=context.get('tags_slug'))
                cache.set(cache_name + ':tags', collection_entity, 60)

        self._get_media_collection(entity=collection_entity)
        collection_title = collection_entity[0].title

        paginator = Paginator(self.media_collection, self.limit)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['collection_title'] = collection_title

        return context

    def _get_media_collection(self, entity: Genre | Tags):
        self.media_collection = []

        if self.type == 'genre':
            movie_list = [{"type": 'movie',
                           "genres": [{"slug": i.slug, "title": i.title} for i in item.genre.all()],
                           'entity': item} for item in Movie.objects.filter(status='p', genre__pk=entity[0].pk)]
            shows_list = [{"type": 'movie',
                           "genres": [{"slug": i.slug, "title": i.title} for i in item.genre.all()],
                           'entity': item} for item in Shows.objects.filter(status='p', genre__pk=entity[0].pk)]
        else:
            movie_list = [{"type": 'movie',
                           "genres": [{"slug": i.slug, "title": i.title} for i in item.genre.all()],
                           'entity': item} for item in Movie.objects.filter(status='p', tags__pk=entity[0].pk)]
            shows_list = [{"type": 'movie',
                           "genres": [{"slug": i.slug, "title": i.title} for i in item.genre.all()],
                           'entity': item} for item in Shows.objects.filter(status='p', tags__pk=entity[0].pk)]
        self.media_collection.extend(movie_list + shows_list)
