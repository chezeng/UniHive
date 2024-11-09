
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("profile/<str:username>", views.view_profile, name="view_profile"),
    # accepts a username parameter
    path("press_follow/<str:username>", views.press_follow, name="press_follow"),
    path("press_unfollow/<str:username>", views.press_unfollow, name="press_unfollow"),
    path("following", views.following, name="following"),
    # path("save_post", views.save_post, name="save_post"),
    path('save_post', views.save_post, name='save_post'),
    path('like_post', views.like_post, name='like_post'),
    path('unlike_post', views.unlike_post, name='unlike_post'),
]
