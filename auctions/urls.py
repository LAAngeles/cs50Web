from django.urls import path
# from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<C_type>", views.category_type, name="category_type"),
    path("listings/<int:Listings_id>", views.Active_Listings, name="Active_Listings"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("delete", views.delete, name="delete"),
    path("close_action", views.close_action, name="close_action"),
    path("Close_Listing/<int:Listings_id>", views.Close_Listing, name="Close_Listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('accounts/login/', views.accounts, name = "accounts")
]
