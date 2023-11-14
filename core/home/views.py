from django.views.generic import TemplateView
from home.utils import DataMixin, IndexBuilder


class Index(DataMixin, TemplateView):
    template_name = 'home/index.html'
    title = 'Главная страница'
    dispatch_ = IndexBuilder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
