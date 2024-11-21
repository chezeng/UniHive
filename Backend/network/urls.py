
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

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
    path('postpage/<int:post_id>',views.postpage,name='postpage'),
    path('mark_button', views.mark_button, name='mark_button'),
    path('unmark_button', views.unmark_button, name='unmark_button'),
    path('search', views.search, name='search'),
    path('maps',views.maps,name='maps'),
    path('points',views.points,name='points'),
    path('points/<int:post_id>',views.points,name='points'),
    path('chat', views.chat, name='chat'),
    path('posts',views.posts, name='posts')
]


if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)