from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.error, name="error"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>", views.topic, name="topic"),
    path("search_results", views.search, name="search"),
    path("create_new", views.new_page, name="new_page"),
    path("edit_page", views.edit_page, name="edit_page"),
    ]
