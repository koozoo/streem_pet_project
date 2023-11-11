from django.views.generic import TemplateView

from home.services import IndexBuilder


class Index(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blocks = []

        for item in IndexBuilder().create():
            blocks.append(item.page_data)

        context['page_items'] = blocks
        print(context)
        return context
