import dataclasses
from typing import List

from movie.models import Movie
from tv_shows.models import Shows, ShowsItem


@dataclasses.dataclass
class PageBlockData:
    title: str
    type: str
    more_video_link: tuple
    videos: list
    entity: Movie | Shows


@dataclasses.dataclass
class PageBlock:

    """
    ! all blocks have a display limit of 10 element

    title: system title block
    type: banner or media_block
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
                       } -> 10 items movie
    page_title = view title on page
    """

    title: str
    type: str
    priority: int
    data_filter: dict
    page_title: str | None = None
    page_data: dict = None

    def __str__(self):
        return f"title: {self.title}, type: {self.type}, priotiry: {self.priority}"


class BlockBuilder:
    _type: list = ['banner', 'media_block']

    def __init__(self, title: str, type: str, priority: int):
        self.title = title
        self.type = type
        self.priority = priority


@dataclasses.dataclass
class Page:
    title: str
    blocks: list[PageBlock]
    meta: dict = None
    ads: dict = None
    keyword: dict = None


class PageBuilder:
    _blocks: dict
    _page_title: str

    def _add_block(self, title, type_, priority, data_filter, page_title):
        self._blocks[title] = PageBlock(
            title=title,
            type=type_,
            priority=priority,
            data_filter=data_filter,
            page_title=page_title
        )

    def _compose_data(self, params: dict):

        data = []

        for k, fiter_params in params.items():
            if fiter_params is not None:
                if k == 'movie':
                    data.append(self._get_movies(**fiter_params))
                else:
                    data.append(self._get_shows(**fiter_params))

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

                result.append(PageBlockData(
                    title=item.title,
                    type=type_,
                    more_video_link=more_video_link,
                    videos=videos,
                    entity=item
                ))
        return result

    def _create_page(self):
        page_block_data = []
        for title, value in self._blocks.items():
            block_data = self._compose_data(params=value.data_filter)

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

    def set_page_title(self, title):
        self._page_title = title

    def get_page_title(self):
        return self._page_title
