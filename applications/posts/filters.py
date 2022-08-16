from .models import Post
from django_filters import rest_framework


class PostFilter(rest_framework.FilterSet):
    created_at = rest_framework.DateFilter(field_name='created_at')

    class Meta:
        model = Post
        fields = ['created_at']
