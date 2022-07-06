from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry_page, name="entry_page"),
    path("errorpage",views.errorpage, name="error_page")
]