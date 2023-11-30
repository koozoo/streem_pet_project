from django.core.cache import cache

import dataclasses
from typing import List

from genre.models import Genre
from movie.models import Movie
from tv_shows.models import Shows, ShowsItem


@dataclasses.dataclass
class PageBlockData:
    title: str
    type: str
    more_video_link: tuple
    videos: list
    genres: list[dict]
    tags_data: list[dict]
    showrunner: dict
    actors: list[dict]
    entity: Movie | Shows


@dataclasses.dataclass
class PageBlock:

    """
    ! all blocks have a display limit of 10 element

    title: system title block
    type: banner | media_block
    priority: The higher the priority, the higher the block is displayed on the site.
    data_filter: {'shows': {'params': {'value'} | None,
                  'movie': {'params': 'value'} | None,}

                   example:
                       {
                       'movie': {'genre': 'anime', 'status': 'p'},
                       'shows': {'genre': 'anime', 'status': 'p'}
                       }  -> 5 items shows and 5 items movie

                       or

                       {'shows': None,
                        'movie': {'genre': 'anime', 'status': 'p'}
                       } -> 10 items movie with genre anime
    page_title: view title on page
    page_data: data for block on page
    component_name: view template data
    """

    title: str
    type: str
    priority: int
    data_filter: dict
    page_title: str | None = None
    page_data: dict = None
    component_name: str = None

    def __str__(self):
        return f"title: {self.title}, type: {self.type}, priotiry: {self.priority}"


@dataclasses.dataclass
class Page:
    title: str
    blocks: list[PageBlock]
    meta: dict = None
    ads: dict = None
    keyword: dict = None
    filter: dict = None


class PageBuilder:
    """

    _blocks: list blocks for render page
    _page_title: page title

    """
    _blocks: dict
    _page_title: str

    def __init__(self, page_title=None, params=None):
        self._page_title = page_title
        self._params = params

    def _add_block(self, title, type_, priority, data_filter, page_title):
        self._blocks[title] = PageBlock(
            title=title,
            type=type_,
            priority=priority,
            data_filter=data_filter,
            page_title=page_title
        )

    def _compose_data(self, params: dict, limit: int):

        data = []

        if params['movie'] is None or params['shows'] is None:
            limit = 10

        for k, fiter_params in params.items():

            if fiter_params is not None:
                if k == 'movie':
                    if self._params is not None:
                        data.append(self._get_movies(limit=limit, **fiter_params))
                    else:
                        data.append(self._get_movies(limit=limit, **fiter_params))
                else:
                    data.append(self._get_shows(limit=limit, **fiter_params))

        if data:
            return data

    def _get_shows(self, offset: int = 0, limit: int = 5, **kwargs):
        return Shows.objects.filter(**kwargs)[offset:limit]

    def _get_movies(self, offset: int = 0, limit: int = 5, **kwargs):
        return Movie.objects.filter(**kwargs)[offset:limit]

    def _compose_page_block_data(self, entity: List[Shows | Movie]):
        result = []

        for media_type_data in entity:
            for item in media_type_data:

                cache_item = f'media_cache:{item.title}'

                cache_item_genre = cache_item + ':genre'
                cache_item_tags = cache_item + ':tags'
                cache_item_actors = cache_item + ':actors'
                cache_item_showrunner = cache_item + ':showrunner'
                cache_item_videos = cache_item + ':videos'

                cache_genre = cache.get(cache_item_genre)
                if cache_genre:
                    genre = cache_genre
                else:
                    genre = [{"slug": i.slug, "title": i.title} for i in item.genre.all()]
                    cache.set(cache_item_genre, genre, 60)

                cache_tags = cache.get(cache_item_tags)
                if cache_tags:
                    tags = cache_tags
                else:
                    tags = [{"slug": i.slug, "title": i.title} for i in item.tags.all()]
                    cache.set(cache_item_tags, tags, 60)

                cache_actors = cache.get(cache_item_actors)
                if cache_actors:
                    actors = cache_actors
                else:
                    actors = [{"slug": i.slug, "name": i.name} for i in item.actors.all()]
                    cache.set(cache_item_actors, actors, 60)

                cache_showrunner = cache.get(cache_item_showrunner)
                if cache_showrunner:
                    showrunner = cache_showrunner
                else:
                    showrunner = item.showrunner
                    cache.set(cache_item_showrunner, showrunner, 60)

                cache_videos = cache.get(cache_item_videos)
                if cache_videos:
                    videos = cache_videos
                else:
                    if isinstance(item, Shows):
                        type_ = 'shows'
                        more_video_link = 'shows:detail_shows', item.slug
                        videos = ShowsItem.objects.filter(shows_id=item.pk)

                    elif isinstance(item, Movie):
                        type_ = 'movie'
                        more_video_link = 'movie:detail_shows', item.slug
                        videos = item.video

                    else:
                        print(f'Unknowns entity: {item}')
                        continue

                    cache.set(cache_item_videos, cache_videos, 60)

                result.append(PageBlockData(
                    title=item.title,
                    type=type_,
                    more_video_link=more_video_link,
                    genres=genre,
                    videos=videos,
                    entity=item,
                    showrunner=showrunner,
                    tags_data=tags,
                    actors=actors
                ))
        return result

    def _create_page(self, limit=5):
        page_block_data = []
        for title, value in self._blocks.items():
            block_data = self._compose_data(params=value.data_filter, limit=limit)

            info = {
                'view_block_title': value.page_title,
                'block_title': title,
                'type': value.type
            }
            data = self._compose_page_block_data(block_data)

            self._blocks[title].page_data = {
                'block_info': info,
                'data': {'data_item': data}
            }
            page_block_data.append(self._blocks[title])

        return page_block_data
