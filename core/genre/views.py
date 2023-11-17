from services.base_collection_mixin import BaseCollection


class MainGenre(BaseCollection):
    template_name = 'home/base-collections.html'
    limit = 20
    type = 'genre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
