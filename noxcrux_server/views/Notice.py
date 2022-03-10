from django.views.generic import TemplateView


class NoticeView(TemplateView):
    template_name = 'notice.html'
