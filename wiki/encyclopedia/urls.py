from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("newpage",views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("<str:entry>", views.entry_page, name="entry_page")
]