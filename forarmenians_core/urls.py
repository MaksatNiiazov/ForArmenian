"""forarmenians_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('blog/', includes('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('i18n/', include('django.conf.urls.i18n')),

    path("", include('forarmenians_app.urls')),
    path("", include('user_auth.urls')),
    path('', include('paypal_app.urls')),
    path("chats/", include('chat.urls')),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('accounts/', include('allauth.urls')),

]
# urlpatterns += i18n_patterns(
#     path("", include('forarmenians_app.urls')),
#     path("", include('user_auth.urls')),
# )
