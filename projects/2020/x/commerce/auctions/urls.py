from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories0, name="categories0"),
    path("categories/<str:category>", views.categories1, name="categories1"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("editwl/<int:listing_id>", views.edit_wl, name="edit_wl"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close")
]
