from django.urls import path, include
from django.contrib import admin
# from yvm.admin import admin_site
from . import views
# from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView


urlpatterns = [
    path("", views.index, name="index"),
    path("summary", views.bycountryAllTexts, name="bycountryAllTexts"),
    path("i18n/", include("django.conf.urls.i18n")),
    path('comment_my_stances/', RedirectView.as_view(url='/comment_my_stances/yvm/position/')),
    path("about/", TemplateView.as_view(template_name="yvm/about.html")),
]

