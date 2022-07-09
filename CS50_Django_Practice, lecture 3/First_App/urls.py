from django.urls import path

from . import views # The "." represents current directory

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greetings")
]