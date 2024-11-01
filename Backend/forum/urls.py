from django.urls import path
from posts.views import PostListView

urlpatterns = [
    path('api/posts/', PostListView.as_view(), name='post-list'),
]
