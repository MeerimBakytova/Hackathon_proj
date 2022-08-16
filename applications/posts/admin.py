from django.contrib import admin

from applications.posts.models import PostImage, Rating, Like, Post, Comment, Favorite

admin.site.register(PostImage)
admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Favorite)


class CommentAdmin(admin.ModelAdmin):
    model = Comment


admin.site.register(Comment, CommentAdmin)


class PostImageInAdmin(admin.TabularInline):
    model = PostImage
    max_num = 5
    min_num = 1
    fields = ['image']


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInAdmin]


admin.site.register(Post, PostAdmin)
