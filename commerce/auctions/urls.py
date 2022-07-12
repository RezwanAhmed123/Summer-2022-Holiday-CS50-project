from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("userinfo/<int:user_id>", views.user_info,name="userinfo"),
    path("edit_myinfo", views.edit_myinfo, name="editmyinfo"),
    path("changepassword", views.changepassword, name="changepassword"),
    path("newlisting", views.new_listing, name="newlisting"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("edit_listing/<int:item_id>", views.edit_listing, name="editlisting"),
    path("add_to_watchlist/<int:item_id>", views.add_to_watchlist, name="addtowatchlist"),
    path("add_comment/<int:item_id>", views.add_comment, name="addcomment"),
    path("bid_status/<int:item_id>", views.bidding, name="bidstatus"),
    path("register", views.register, name="register"),
]

urlpatterns += staticfiles_urlpatterns()