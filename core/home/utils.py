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
    __default_content_block = {
        'main_banner': None,
        'top_10': None,
        'most_view': None,
        'second_banner': None,
        'anime': None,
    }

    def __init__(self, request):
        self.request = request

    def _main_banner(self, block_title: str = None):
        movies, shows = self._get_banner_movie(), self._get_banner_shows()
        block_data = {block_title: []}

        for item in movies:
            title = item.title
            type_ = 'movie'
            more_video_link = ('movie:detail_movie', item.slug)
            videos = item.video

            block_data[block_title] += [PageBlockData(title=title,
                                                      type=type_,
                                                      more_video_link=more_video_link,
                                                      videos=videos,
                                                      entity=item)]

        for item in shows:
            title = item.title
            type_ = 'shows'
            more_video_link = ('shows:detail_shows', item.slug)
            videos = shows_models.ShowsItem.objects.filter(shows_id=item.pk)

            block_data[block_title] += [PageBlockData(title=title,
                                                      type=type_,
                                                      more_video_link=more_video_link,
                                                      videos=videos,
                                                      entity=item)]

        return block_data

    def _top_10(self):
        ...

    def _most_views(self):
        ...

    def _second_banner(self):
        ...

    def _anime(self):
        ...

    def _get_banner_shows(self, offset: int = 0, limit: int = 5):
        return shows_models.Shows.objects.filter(status='p', total_watch__gte=0)[offset:limit]

    def _get_banner_movie(self, offset: int = 0, limit: int = 5):
        return movie_models.Movie.objects.filter(status='p', total_watch__gte=0)[offset:limit]

    def _get_cache_shows(self):
        return movie_models.Movie.objects.filter(status='p')

    def _get_cache_movie(self):
        return shows_models.Shows.objects.filter(status='p')

    def build_home_page(self):
        page_data = []
        for block_key, block_value in self.__default_content_block.items():

            match block_key:
                case 'main_banner':
                    self.__default_content_block[block_key] = self._main_banner(block_title='main_banner')[block_key]
                case 'top_10':
                    self.__default_content_block[block_key] = self._main_banner(block_title='top_10')[block_key]
                case 'most_view':
                    self.__default_content_block[block_key] = self._main_banner(block_title='most_view')[block_key]
                case 'second_banner':
                    self.__default_content_block[block_key] = self._main_banner(block_title='second_banner')[block_key]
                case 'anime':
                    self.__default_content_block[block_key] = self._main_banner(block_title='anime')[block_key]
                case '_':
                    self.__default_content_block[block_key] = self._main_banner(block_title='default')[block_key]

        return self.__default_content_block
