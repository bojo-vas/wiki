from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.error, name="error"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>", views.topic, name="topic"),
    path("search_results", views.search, name="search"),
]
