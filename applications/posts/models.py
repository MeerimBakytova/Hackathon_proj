from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from applications.account.models import CustomUser

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(CustomUser, default=True, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class PostImage(models.Model):
    image = models.ImageField(upload_to='posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='image')


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author} на пост {self.post}"


class Rating(models.Model):
    owner = models.ForeignKey(CustomUser,
                              on_delete=models.CASCADE,
                              related_name='ratings',
                              verbose_name='Владелец рейтинга'
                              )
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                related_name='ratings')
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ], default=1
    )

    def __str__(self):
        return f'{self.comment} - {self.rating}'


class Like(models.Model):
    owner = models.ForeignKey(CustomUser,
                              on_delete=models.CASCADE,
                              related_name='likes',
                              verbose_name='Пользователь')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='like')
    like = models.BooleanField('Лайк', default=False)

    def __str__(self):
        return f'{self.like}'


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorite')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorite')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.post}'


