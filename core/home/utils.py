import dataclasses

from django.db.models import QuerySet
from movie import models as movie_models
from tv_shows import models as shows_models


@dataclasses.dataclass
class PageBlockData:
    title: str
    type: str
    more_video_link: tuple
    videos: list
    entity: movie_models.Movie | shows_models.Shows


class HomePageBuilder:
    _collections: list
    __default_content_block = {
        'main_banner': None,
        'top_10': None,
        'most_view': None,
        'anime': None,
    }

    def __init__(self, request):
        self.request = request

    def _main_banner(self):
        movies, shows = self._get_banner_movie(), self._get_banner_shows()
        block_data = {'data_item': []}

        for item in movies:
            title = item.title
            type_ = 'movie'
            more_video_link = ('movie:detail_movie', item.slug)
            videos = item.video

            block_data['data_item'] += [PageBlockData(title=title,
                                                      type=type_,
                                                      more_video_link=more_video_link,
                                                      videos=videos,
                                                      entity=item)]

        for item in shows:
            title = item.title
            type_ = 'shows'
            more_video_link = ('shows:detail_shows', item.slug)
            videos = shows_models.ShowsItem.objects.filter(shows_id=item.pk)

            block_data['data_item'] += [PageBlockData(title=title,
                                                      type=type_,
                                                      more_video_link=more_video_link,
                                                      videos=videos,
                                                      entity=item)]

        return block_data

    def _top_10(self):
        ...

    def _most_views(self):
        ...

    def _anime(self):
        ...

    def _collect_data(self, block_key):
        self._collections.append(self.__default_content_block[block_key])

    def _get_banner_shows(self, offset: int = 0, limit: int = 5):
        return shows_models.Shows.objects.filter(status='p', total_watch__gte=0)[offset:limit]

    def _get_banner_movie(self, offset: int = 0, limit: int = 5):
        return movie_models.Movie.objects.filter(status='p', total_watch__gte=0)[offset:limit]

    def build_home_page(self):
        self._collections = []

        for block_key, block_value in self.__default_content_block.items():

            match block_key:
                case 'main_banner':
                    b_info = {
                        'view_block_title': None,
                        'block_title': block_key
                    }
                    b_data = self._main_banner()

                    self.__default_content_block[block_key] = {"block_info": b_info, "data": b_data}
                    self._collect_data(block_key=block_key)

                case 'top_10':
                    b_info = {
                        'view_block_title': 'Топ 10',
                        'block_title': block_key
                    }
                    b_data = self._main_banner()
                    self.__default_content_block[block_key] = {"block_info": b_info, "data": b_data}
                    self._collect_data(block_key=block_key)
                case 'most_view':
                    b_info = {
                        'view_block_title': 'Топ по просмотрам',
                        'block_title': block_key
                    }
                    b_data = self._main_banner()
                    self.__default_content_block[block_key] = {"block_info": b_info, "data": b_data}
                    self._collect_data(block_key=block_key)

                # case 'anime':
                #     self.__default_content_block[block_key] = self._main_banner(block_title='anime',
                #                                                                 view_title_on_page='Аниме')[block_key]
                # case '_':
                #     self.__default_content_block[block_key] = self._main_banner(block_title='default',
                #                                                                 view_title_on_page='Случайно подабраное')[block_key]

        return self._collections
