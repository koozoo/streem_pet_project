from django.views.generic import TemplateView


class MediaMixin(TemplateView):
    template_name: str = None
    type: str = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


    def _build_context(self):
        ...