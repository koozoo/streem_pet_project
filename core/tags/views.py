from django.views.generic import TemplateView

from movie.models import Movie
from tv_shows.models import Shows
from tags.models import Tags


class MainGenre(TemplateView):
    template_name = 'home/base-collections.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        genre_data = self._get_data(slug=kwargs['tags_slug'])[0]
        context['collection_title'] = genre_data['title']
        context['collection_image'] = genre_data['image']
        context['data'] = 'asd'
        return context

    def _get_data(self, slug):
        tags_collection = Tags.objects.filter(status='p', slug=slug)
        data_genre = [{'slug': item.slug, 'title': item.title, 'image': item.images} for item in tags_collection]
        media_data = [item for item in self._get_media(tags=tags_collection[0])]
        print(media_data)
        return data_genre

    def _get_media(self, tags):
        genre_collection = []
        movie_collections = [genre_collection.append(item) for item in Movie.objects.filter(status='p', tags=tags)]
        shows_collections = [genre_collection.append(item) for item in Shows.objects.filter(status='p', tags=tags)]
        return genre_collection
