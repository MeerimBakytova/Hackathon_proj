from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from . import permissions
from .filters import PostFilter
from .models import Post, Like, Rating, Comment
from .permissions import IsOwnerOrReadOnly, IsCommentAuthor
from .serializers import PostSerializer, RatingSerializer, CommentSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['author', 'created_at']
    ordering_fields = ['author', 'id']
    search_fields = ['author', 'created_at']

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('day', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset

        # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         self.permission_classes = [permissions.AllowAny]
    #     elif self.action in ['create']:
    #         self.permission_classes = [permissions.IsAuthenticated]
    #     elif self.action in ['update', 'partial_update', 'destroy']:
    #         self.permission_classes = [IsOwnerOrReadOnly]
    #     return [permission() for permission in self.permission_classes]

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        try:
            like_object, _ = Like.objects.get_or_create(owner=request.user, post_id=pk)
            like_object.like = not like_object.like
            like_object.save()
            status = 'liked'

            if like_object.like:
                return Response({'status': status})
            status = 'unliked'
            return Response({'status': status})
        except:
            return Response('Нет такого поста')

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk, *args, **kwargs):
        serializers = RatingSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(owner=request.user, comment_id=pk)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status=201)

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk, *args, **kwargs):
        review = self.get_object()
        favorite_obj, _ = Like.objects.get_or_create(owner=request.user, post_id=pk)
        favorite_obj.like = not favorite_obj.like
        favorite_obj.save()
        status = 'favorite'
        if not favorite_obj.like:
            status = 'not in the favorites'
        return Response({'status': status})


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RetrieveEditDestroyCommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
