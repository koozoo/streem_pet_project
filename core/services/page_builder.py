import dataclasses

from movie.models import Movie
from tv_shows.models import Shows


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
    models: dict = None
    dispatcher: dict = None
