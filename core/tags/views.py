from services.base_collection_mixin import BaseCollection


class MainTags(BaseCollection):
    template_name = 'home/base-collections.html'
    limit = 20
    type = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = context.get('page_obj')

        return context
