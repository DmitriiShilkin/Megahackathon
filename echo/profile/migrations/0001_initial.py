# Generated by Django 4.2.7 on 2023-11-23 13:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import profile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Последний вход')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Фамилия')),
                ('city', models.CharField(blank=True, max_length=150, null=True, verbose_name='Город')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Статус администратора')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Статус персонала')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Статус суперпользователя')),
                ('hide_email', models.BooleanField(default=True, verbose_name='Скрыть email')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='О себе')),
                ('image', models.ImageField(default=profile.models.get_default_profile_image, upload_to=profile.models.get_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png']), profile.models.validate_size_image], verbose_name='Фотография')),
                ('phone', models.CharField(blank=True, max_length=13, null=True, verbose_name='Телефон')),
                ('vk', models.CharField(blank=True, max_length=50, null=True, verbose_name='ВКонтакте')),
                ('telegram', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telegram')),
                ('whatsapp', models.CharField(blank=True, max_length=50, null=True, verbose_name='WhatsApp')),
                ('facebook', models.CharField(blank=True, max_length=50, null=True, verbose_name='Facebook')),
                ('twitter', models.CharField(blank=True, max_length=50, null=True, verbose_name='Twitter')),
                ('instagram', models.CharField(blank=True, max_length=50, null=True, verbose_name='Instagram')),
                ('favourite', models.ManyToManyField(blank=True, related_name='favourite_posts', to='posts.post', verbose_name='Избранные публикации')),
                ('subscribed_categories', models.ManyToManyField(blank=True, related_name='category_subscribers', to='posts.category', verbose_name='Подписки на категории')),
                ('subscribed_users', models.ManyToManyField(blank=True, related_name='user_subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Подписки на пользователей')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
