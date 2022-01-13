from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from . import views as app_views

urlpatterns = [
    path("", app_views.index, name="index"),
    path("signin/", app_views.signin, name="signin"),
    path("signout/", auth_views.LogoutView.as_view(template_name="stock_market/index.html"), name="signout"),
    path("signup/", app_views.signup, name="signup"),
    path("insert_into_db/", app_views.insert_into_db, name="insert_into_db"),
    re_path(r"stock_details/(?P<slug_name>\w+)", app_views.stock_details, name="stock_details"),
    path("search/", app_views.search, name="search"),
    re_path(r"submit_query/(?P<stock_id>\w+)", app_views.submit_query, name="submit_query"),
]