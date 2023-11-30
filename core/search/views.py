import json

from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from categories.models import Categories
from genre.models import Genre
from movie.models import Movie
from tv_shows.models import Shows


class Filter:
    _CACHE_EXPIRED = 60

    def __init__(self, params: dict = None):
        if params is not None:
            self.data = params['request']
        else:
            self.data = None

    def _is_checked(self):
        return [filter_k for filter_k, filter_v in self.data.items() if filter_v]

    def _get_genre(self):
        genre_cache_name = f"genre:{self.data['genre']['slug']}"
        genre_cache = cache.get(genre_cache_name)
        if genre_cache is not None:
            return genre_cache
        else:
            genre = Genre.objects.filter(status='p', slug=self.data['genre']['slug'])
            cache.set(genre_cache_name, genre, self._CACHE_EXPIRED)
            return genre

    def _get_media_collections(self, category: str = None, genre: str = None, order_by: str = None):

        params = {'status': 'p'}
        if order_by is not None:
            ob = f"{self.data['sort']['slug']}"
        else:
            ob = "total_watch"

        if genre is not None:
            gn = self._get_genre()
        else:
            gn = genre

        if category is not None:
            cat = f"{self.data['category']['slug']}"
        else:
            cat = category

        if self.data:
            cache_name = f'filter:media_collections:{hash(str(self.data))}'
        else:
            cache_name = 'filter:media_collections:default'

        media_cache_name = cache.get(cache_name, None)
        if media_cache_name:
            media = media_cache_name
        else:
            media = self._query(category=cat, genre=gn, order_by=ob, cache_name=media_cache_name, **params)

        return media

    def _query(self, cache_name: str, order_by: str, category: str, genre: Genre = None, **params):
        if genre is not None:
            params.update({'genre': genre[0].pk})
        if category is not None:
            if category == 'movie':
                media = Movie.objects.filter(**params).order_by(f"-{order_by}").values()
            else:
                media = Shows.objects.filter(**params).order_by(f"-{order_by}").values()

        else:
            shows = Shows.objects.filter(**params).order_by(f"-{order_by}").values()
            movie = Movie.objects.filter(**params).order_by(f"-{order_by}").values()

            tmp = list(shows) + list(movie)
            test = {item[order_by]: item for item in tmp}

            media = [item[1] for item in sorted(test.items(), reverse=True)]
            cache.set(cache_name, media, self._CACHE_EXPIRED)

        return media

    def start(self):
        if self.data is not None:
            param = self._is_checked()
            query_params = {}
            for i in param:
                match i:
                    case 'genre':
                        query_params.update({"genre": "checked"})
                    case 'sort':
                        query_params.update({"order_by": "checked"})
                    case 'category':
                        query_params.update({"category": "checked"})

            return self._get_media_collections(**query_params)
        else:
            return self._get_media_collections()


class FilterForm(View):
    _CACHE_EXPIRED = 60
    _PAGINATION_LIMIT = 4

    def get(self, request, *args, **kwargs):
        if request.GET:
            request_data = [json.loads(item[0]) for item in request.GET.items()][0]
            print("request_data", request_data)
            if request_data:
                context = self._get_media_data(**request_data)
            else:
                context = self._get_media_data()
            return render(request, 'home/media_collections_content.html', context=context)
        else:
            return render(request, 'home/media_collections_loader.html')

    def _get_media_data(self, **filter_params):

        if filter_params:
            fil = Filter(filter_params)
            media = fil.start()
        else:
            fil = Filter()
            media = fil.start()

        paginator = Paginator(media, self._PAGINATION_LIMIT)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {"media": media,
                   "page_obj": page_obj}

        return context
