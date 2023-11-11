from typing import List

from movie.models import Movie
from services.page_builder import PageBlock, PageBlockData
from tv_shows.models import Shows, ShowsItem


class IndexBuilder:
    _blocks: dict

    # CUSTOM METHODS #

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

    def _init_blocks(self):
        """
            initianal blocks
        """

        self._blocks = {}

        self._main_banner()
        self._top_10()
        self._top_anime()
        self._top_fantastic()

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

    def create(self):
        self._init_blocks()

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
