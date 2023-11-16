from services.page_builder import PageBlock, Page, PageBuilder

menu = {
    'home': {
        'title': 'Главная',
        'url': 'home',
        'is_active': False
    },
    'movie': {
        'title': 'Фильмы',
        'url': 'movie',
        'is_active': False
    },
    'shows': {
        'title': 'Сериалы',
        'url': 'shows',
        'is_active': False
    },
}


class DataMixin:
    title: str = None
    page_items = None
    dispatch_ = None
    extra_context = {}
    blocks: list = None
    genre: str = None
    tags: str = None

    def __init__(self):
        if self.title:
            self.extra_context['title'] = self.title

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

        if self.page_items:
            self.extra_context['page_items'] = self.page_items
        else:
            if self.tags:
                ...

            if self.genre:
                ...

            try:
                self._get_page_data(page_builder_callback=self.dispatch_)
                self.extra_context['page_items'] = self.blocks
            except TypeError:
                print(TypeError)

    def get_mixin_context(self):
        return self.extra_context

    def _get_config(self, config_name: str):
        ...

    def _get_page_data(self, page_builder_callback, genre: str = None, tags: str = None):
        self.blocks = []

        if genre is not None:
            page = page_builder_callback(page_title=self.title, params=self.genre).create()
        elif tags is not None:
            page = page_builder_callback(page_title=self.title, params=self.tags).create()
        else:
            page = page_builder_callback(page_title=self.title).create()

        for item in page.blocks:
            self.blocks.append(item.page_data)


class IndexBuilder(PageBuilder):

    def __init__(self, page_title, params=None):
        super().__init__(page_title, params)

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
        priority = 5
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
