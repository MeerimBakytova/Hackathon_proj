import instance as instance
from rest_framework import serializers
from rest_framework.utils import representation

from .models import Post, PostImage, Comment, Favorite, Rating


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('image',)


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    # image = PostImageSerializer()

    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        requests = self.context.get('request')
        image = requests.FILES
        post = Post.objects.create(**validated_data)
        for image in image.getlist('image'):
            PostImage.objects.create(post=post, image=image)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = PostImageSerializer(instance.image.all(), many=True, context=self.context).data
        representation['like'] = instance.like.filter(like=True).count()
        representation['comment'] = CommentSerializer(Comment.objects.filter(post_id=instance), many=True).data
        representation['favorite'] = FavoriteSerializer(Favorite.objects.filter(post_id=instance), many=True).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total_rating = [i.rating for i in instance.rating.all()]
        if len(total_rating) != 0:
            representation['total_rating'] = sum(total_rating) / len(total_rating)
        else:
            representation['total_rating'] = ""


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"
