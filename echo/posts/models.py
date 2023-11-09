from django.core.validators import MinLengthValidator
from django.db import models

from sign.models import User
from sign.models import get_image_path


# Модель для категорий
class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name.capitalize()


# Модель для публикаций
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)
    text = models.TextField(
        validators=[
            MinLengthValidator(50, 'Это поле должно содержать минимум 50 символов')
        ],
        verbose_name='Публикация',
    )
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to=get_image_path)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    favourite = models.ManyToManyField(User, blank=True, related_name='favourites')
    category = models.ManyToManyField(Category, related_name='posts', verbose_name='Категория')

    def __str__(self):
        return self.text[:50]


# Модель для комментариев
class Comment(models.Model):
    text = models.CharField(max_length=254, blank=True, verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Модель для лайков
class Like(models.Model):
    value = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
