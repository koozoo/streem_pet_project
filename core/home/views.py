from django.views.generic import TemplateView
from home import utils


class Index(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        home_page_builder = utils.HomePageBuilder(request=self.request)

        for item_name, item_value in home_page_builder.build_home_page().items():
            print(item_name, item_value)
            context[item_name] = item_value

        return context
