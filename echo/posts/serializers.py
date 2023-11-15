from rest_framework import serializers
# from drf_writable_nested import WritableNestedModelSerializer

from .models import Post, Category, Comment, Like, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'url',
            'id',
            'name',
        ]


# Cериализатор модели публикаций
class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, allow_empty=False)
    image = serializers.URLField(label='Image URL', allow_blank=True)

    class Meta:
        model = Post
        depth = 1
        fields = [
            'url',
            'id',
            'headline',
            'text',
            'image',
            'category',
        ]

    # переопредяем метод post, чтобы передать авторизованного пользователя и добавить связь со многими категориями
    def create(self, validated_data, **kwargs):
        # получаем данные публикации из валидатора
        categories = validated_data.pop('category')
        user = validated_data.pop('user')
        headline = validated_data.pop('headline')
        text = validated_data.pop('text')
        image = validated_data.pop('image')
        # создаем публикацию
        post = Post.objects.create(headline=headline, text=text, image=image, author=user)
        # добавляем связи с категориями
        if categories:
            post.category.set(categories)

        return post


# Сериализатор модели отзывов
class ReviewSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    image = serializers.URLField(label='image URL', allow_blank=True)

    class Meta:
        model = Review
        depth = 1
        fields = [
            'url',
            'id',
            'headline',
            'text',
            'rating',
            'image',
            'post',
        ]

    # переопредяем метод post, чтобы передать авторизованного пользователя
    def create(self, validated_data, **kwargs):
        # получаем данные отзыва из валидатора
        user = validated_data.pop('user')
        review = Review.objects.create(**validated_data, user=user)

        return review


# Сериализатор модели комментариев
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), allow_null=True)
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), allow_null=True)

    class Meta:
        model = Comment
        depth = 1
        fields = [
            'url',
            'id',
            'text',
            'post',
            'review',
        ]

    # переопредяем метод post, чтобы передать авторизованного пользователя
    def create(self, validated_data, **kwargs):
        # получаем данные отзыва из валидатора
        user = validated_data.pop('user')
        text = validated_data.pop('text')
        post = validated_data.pop('post')
        review = validated_data.pop('review')

        # если передана связь с моделью post, создаем комментарий к post
        if post and not review:
            comment = Comment.objects.create(text=text, user=user, post=post)
            return comment

        # если передана связь с моделью review, создаем комментарий к review
        if review and not post:
            comment = Comment.objects.create(text=text, user=user, review=review)
            return comment

        # если не передано ни одной связи с моделью
        if not (post or review):
            raise serializers.ValidationError('Поля post и review не могут быть пустыми одновременно.')

        # если передана связь сразу на обе модели
        if post and review:
            raise serializers.ValidationError('Поля post и review не могут быть заполнены одновременно.')

    # переопределяем метод patch, чтобы выполнить проверки связей с моделями
    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.post = validated_data.get("post", instance.post)
        instance.review = validated_data.get("review", instance.review)

        # если не передано ни одной связи с моделью
        if not (instance.post or instance.review):
            raise serializers.ValidationError('Поля post и review не могут быть пустыми одновременно.')

        # если передана связь сразу на обе модели
        if instance.post and instance.review:
            raise serializers.ValidationError('Поля post и review не могут быть заполнены одновременно.')

        instance.save()

        return instance


# Сериализатор модели лайков
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'value',
        ]
