from typing import List

from movie.models import Movie
from services.page_builder import PageBlock, PageBlockData, PageBuilder, Page
from tv_shows.models import Shows, ShowsItem


class IndexBuilder(PageBuilder):

    def __init__(self, page_title):
        super().__init__(page_title)

    def _main_banner(self):
        title = 'main_banner'
        type_ = 'banner'
        priority = 1
        data_filter = {'movie': {'total_watch__gte': 0,
                                 'status': 'p'},
                       'shows': {'total_watch__gte': 0,
                                 'status': 'p'},
                       }

        self._blocks[title] = PageBlock(
            title=title,
            type=type_,
            priority=priority,
            data_filter=data_filter
        )

    def _top_10(self):
        title = 'top_10'
        page_title = 'Топ 10'
        type_ = 'media_block'
        priority = 2
        data_filter = {'movie': {'total_watch__lte': 5,
                                 'status': 'p'},
                       'shows': {'total_watch__lte': 5,
                                 'status': 'p'},
                       }

        self._add_block(title=title, type_=type_, priority=priority, data_filter=data_filter, page_title=page_title)

    def _top_anime(self):
        title = 'top_anime'
        page_title = 'Топ Аниме'
        type_ = 'media_block'
        priority = 3
        data_filter = {'movie': {'total_watch__gte': 0,
                                 'status': 'p'},
                       'shows': {'showrunner': 1,
                                 'status': 'p'},
                       }

        self._add_block(title=title, type_=type_, priority=priority, data_filter=data_filter, page_title=page_title)

    def _top_fantastic(self):
        # EDIT FIELDS
        title = 'top_fantastic'
        page_title = 'Лучшая Фантастика'
        type_ = 'media_block'
        priority = 4
        data_filter = {'movie': None,
                       'shows': {'showrunner': 2,
                                 'status': 'p'},
                       }
        self._add_block(title=title, type_=type_, priority=priority, data_filter=data_filter, page_title=page_title)

    def _top_fantastic(self):
        # EDIT FIELDS
        title = 'top_fantastic'
        page_title = 'Лучшая Фантастика'
        type_ = 'media_block'
        priority = 4
        data_filter = {'movie': None,
                       'shows': {'showrunner': 2,
                                 'status': 'p'},
                       }
        self._add_block(title=title, type_=type_, priority=priority, data_filter=data_filter, page_title=page_title)

    # SYSTEM METHODS #

    def _init_blocks(self):
        """
            initianal blocks
        """

        self._blocks = {}

        self._main_banner()
        self._top_10()
        self._top_anime()
        self._top_fantastic()

    def create(self) -> Page:
        self._init_blocks()

        page_data = self._create_page()

        return Page(
            title=self._page_title,
            blocks=page_data
        )
