from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_info/<str:listing_name>", views.listing_info, name="listing_info"),
    path("create_comment/<str:listing_name>", views.create_comment, name="create_comment"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("bidding_page/<str:listing_name>", views.bidding_page, name="bidding_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
