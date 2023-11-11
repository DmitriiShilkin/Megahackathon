from PIL import Image

from django.db import models
from django.contrib.auth.models import User


# функция получения пути для сохранения фотографий, чтобы было понятно, к какому instance они относятся
def get_image_path(instance, file):
    return f'photos/{instance}/{file}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, verbose_name='О себе')
    image = models.ImageField(blank=True, null=True, upload_to=get_image_path, verbose_name='Фотография')
    phone = models.CharField(max_length=13, blank=True, null=True, verbose_name='Телефон')
    vk = models.CharField(max_length=50, null=True, blank=True, verbose_name='ВКонтакте')
    telegram = models.CharField(max_length=50, null=True, blank=True, verbose_name='Telegram')
    whatsup = models.CharField(max_length=50, null=True, blank=True, verbose_name='WhatsApp')
    facebook = models.CharField(max_length=50, null=True, blank=True, verbose_name='Facebook')
    twitter = models.CharField(max_length=50, null=True, blank=True, verbose_name='Twitter')
    instagram = models.CharField(max_length=50, null=True, blank=True, verbose_name='Instagram')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
