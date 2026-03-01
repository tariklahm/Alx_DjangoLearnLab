from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


class PostPagination(PageNumberPagination):
    page_size = 5

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


User = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed_view(request):
    following_users = request.user.following.all()

    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        return Response({"message": "Post already liked"}, status=400)

    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb="liked your post",
        target_content_type=ContentType.objects.get_for_model(Post),
        target_object_id=post.id
    )

    return Response({"message": "Post liked successfully"})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    like = Like.objects.filter(user=request.user, post=post).first()
    if not like:
        return Response({"message": "Post not liked"}, status=400)

    like.delete()
    return Response({"message": "Post unliked successfully"})