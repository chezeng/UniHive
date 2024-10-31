from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post

class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all().values('id', 'title', 'content', 'author__username', 'created_at')
        return Response(posts)
