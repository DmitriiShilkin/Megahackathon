from django.db import models
from django.contrib.auth.models import User as Usr

# from posts.models import Category


# функция получения пути для сохранения фотографий, чтобы было понятно, к какому instance они относятся
def get_image_path(instance, file):
    return f'photos/{instance}/{file}'


# Кастомная модель пользователя на основе стандартной из Django
class User(models.Model):
    user = models.OneToOneField(Usr, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, null=True, verbose_name='Фотография', upload_to=get_image_path)
    description = models.TextField(blank=True, null=True, verbose_name='О себе')
    media = models.TextField(blank=True, null=True, verbose_name='Социальные сети')
    phone = models.CharField(max_length=13, blank=True, null=True, verbose_name='Телефон')
    # favourite = models.ManyToManyField(to='Post', blank=True, related_name='favourites')
    # subscriptions = models.ManyToManyField(to='Category', blank=True, related_name='categories')

    def __str__(self):
        return self.user.username
