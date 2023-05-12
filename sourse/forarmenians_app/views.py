from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "mainPage/index.html"


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
