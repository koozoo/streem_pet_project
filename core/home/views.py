from django.views.generic import TemplateView
from home import utils


class Index(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blocks = []
        home_page_builder = utils.HomePageBuilder(request=self.request)

        for item in home_page_builder.build_home_page():
            print(item)
            blocks.append(item)

        context['page_items'] = blocks
        print(context)
        return context
