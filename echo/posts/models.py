from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg, Q

from profile.models import Profile
from profile.models import get_image_path


# Модель для айпи адресов
class Ip(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


# Модель для категорий
class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    subscribers = models.ManyToManyField(Profile, blank=True, related_name='categories')

    def __str__(self):
        return self.name.capitalize()


# Модель для публикаций
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    headline = models.CharField(verbose_name='Заголовок', max_length=254)
    text = models.TextField(
        validators=[
            MinLengthValidator(50, 'Это поле должно содержать минимум 50 символов')
        ],
        verbose_name='Содержание',
    )
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to=get_image_path)
    is_published = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    views = models.ManyToManyField(Ip, related_name='post_views', blank=True)
    favourite = models.ManyToManyField(Profile, related_name='favourite_posts', blank=True)
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

    # def total_likes(self, value):
    #     likes = Like.objects.filter(Q(post_id=self.pk) & Q(value=value)).count()
    #
    #     return likes

    def total_comments(self):
        comments = Comment.objects.filter(post_id=self.pk).count()

        return comments

    def set_published(self):
        self.is_published = True
        self.save()


# Модель для отзывов
class Review(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)
    headline = models.CharField(verbose_name='Заголовок', max_length=254)
    text = models.TextField(
        validators=[
            MinLengthValidator(20, 'Это поле должно содержать минимум 20 символов')
        ],
        verbose_name='Содержание',
    )
    rating = models.IntegerField(verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to=get_image_path)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.headline.capitalize()


# Модель для комментариев
class Comment(models.Model):
    text = models.CharField(max_length=254, verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.text[:20]


# Модель для лайков
class Like(models.Model):
    value = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # def plus_like(self):
    #     if self.value is None or self.value == 0:
    #         self.value = 1
    #
    #     if self.value == 1:
    #         self.value = 0
    #
    #     return self.value
    #
    # def dislike(self):
    #     if self.value is None or self.value == 0:
    #         self.value = -1
    #
    #     if self.value == -1:
    #         self.value = 0
    #
    #     return self.value
