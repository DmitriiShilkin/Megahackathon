from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg, Sum, Q

from profile.models import Profile
from profile.models import get_image_path


# Модель для айпи адресов
class Ip(models.Model):
    ip = models.CharField(max_length=100, verbose_name='IP')

    def __str__(self):
        return self.ip


# Модель для категорий
class Category(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='Название')
    subscribers = models.ManyToManyField(Profile, blank=True, related_name='categories', verbose_name='Подписчики')

    def __str__(self):
        return self.name.capitalize()


# Модель для публикаций
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    published = models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')
    modified = models.DateTimeField(blank=True, null=True, verbose_name='Дата измнения')
    headline = models.CharField(verbose_name='Заголовок', max_length=254)
    text = models.TextField(
        validators=[
            MinLengthValidator(50, 'Это поле должно содержать минимум 50 символов')
        ],
        verbose_name='Содержание',
    )
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to=get_image_path)
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор')
    views = models.ManyToManyField(Ip, related_name='post_views', blank=True, verbose_name='Просмотры')
    favourite = models.ManyToManyField(Profile, related_name='favourite_posts', blank=True, verbose_name='Избранное')
    category = models.ManyToManyField(Category, related_name='posts', verbose_name='Категория')

    class Meta:
        ordering = ('-published', '-created')

    def __str__(self):
        return self.headline.capitalize()

    def update_rating(self):
        # получаем все отзывы на данную публикацию
        reviews = Review.objects.filter(post_id=self.pk)
        # вычисляем среднее арифметическое рейтинга всех отзывов на данную публикацию
        self.rating = reviews.aggregate(Avg('rating'))['rating__avg']
        self.save()

    def total_views(self):
        return self.views.count()

    def set_published(self):
        self.is_published = True
        self.save()

    def total_comments(self):
        comments = Comment.objects.filter(post_id=self.pk).count()
        return comments

    def total_likes(self):
        # Забираем queryset с записями больше 0
        likes = Vote.objects.filter(Q(value__gt=0) & Q(post_id=self.pk)).count()
        return likes

    def total_dislikes(self):
        # Забираем queryset с записями меньше 0
        dislikes = Vote.objects.filter(Q(value__lt=0) & Q(post_id=self.pk)).count()
        return dislikes


# Модель для отзывов
class Review(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')
    headline = models.CharField(verbose_name='Заголовок', max_length=254)
    text = models.TextField(
        validators=[
            MinLengthValidator(20, 'Это поле должно содержать минимум 20 символов')
        ],
        verbose_name='Содержание',
    )
    rating = models.IntegerField(verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to=get_image_path)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Публикация')

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.headline.capitalize()

    def total_comments(self):
        comments = Comment.objects.filter(review_id=self.pk).count()
        return comments

    def total_likes(self):
        # Забираем queryset с записями больше 0
        likes = Vote.objects.filter(Q(value__gt=0) & Q(review_id=self.pk)).count()
        return likes

    def total_dislikes(self):
        # Забираем queryset с записями меньше 0
        dislikes = Vote.objects.filter(Q(value__lt=0) & Q(review_id=self.pk)).count()
        return dislikes


# Модель для комментариев
class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')
    text = models.CharField(max_length=254, verbose_name='Комментарий')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Публикация')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Отзыв')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.text[:20]

    def total_likes(self):
        # Забираем queryset с записями больше 0
        likes = Vote.objects.filter(Q(value__gt=0) & Q(comment_id=self.pk)).count()
        return likes

    def total_dislikes(self):
        # Забираем queryset с записями меньше 0
        dislikes = Vote.objects.filter(Q(value__lt=0) & Q(comment_id=self.pk)).count()
        return dislikes


# Модель для лайков и дизлайков
class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')
    value = models.SmallIntegerField(verbose_name='Голос', choices=VOTES)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Публикация')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Отзыв')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.user}: {self.get_value_display()}'
