from django.views.generic import TemplateView


class Logs(TemplateView):
    """Show list of server logs"""

    template_name = 'admin/logs.html'


class Log(TemplateView):
    """Show log content"""

    template_name = 'admin/log.html'

    def get_context_data(self, **kwargs):
        """Pass log content to template"""
        context = super().get_context_data(**kwargs)
        file = kwargs['log']
        with open(F'/var/log/{file}.log', 'r', encoding='UTF8') as log:
            context['content'] = log.read().strip('\n')
        return context