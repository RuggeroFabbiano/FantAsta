from django.views.generic import TemplateView


class Log(TemplateView):
    """Show log content"""

    template_name = 'admin/log.html'

    def get_context_data(self, **kwargs):
        """Pass log content to template"""
        context = super().get_context_data(**kwargs)
        with open('/logs/gunicorn.log', 'r', encoding='UTF8') as log:
            context['content'] = log.read().strip('\n')
        return context