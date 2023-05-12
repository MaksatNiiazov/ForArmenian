from django.urls import path
from django.views.generic import TemplateView

from forarmenians_app.views import MainPageView

urlpatterns = [
    path('main/', MainPageView.as_view()),
    path('ads/', TemplateView.as_view(template_name='abc/abc.html'))
]

