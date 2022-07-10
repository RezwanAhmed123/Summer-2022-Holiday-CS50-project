from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("userinfo/<int:user_id>", views.user_info,name="userinfo"),
    path("edit_myinfo",views.edit_myinfo, name="editmyinfo"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("newlisting", views.new_listing, name="newlisting"),
    path("register", views.register, name="register"),
]
