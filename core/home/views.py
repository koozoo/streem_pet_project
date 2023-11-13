from django.views.generic import TemplateView

from home.services import IndexBuilder


class Index(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blocks = []
        page = IndexBuilder(page_title='Главная страница', ).create()

        for item in page.blocks:
            blocks.append(item.page_data)

        context['title'] = page.title
        context['keyword'] = page.keyword
        context['page_items'] = blocks
        return context
