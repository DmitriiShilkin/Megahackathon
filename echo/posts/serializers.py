# import datetime
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from .models import Post, Category, Comment, Vote, Review


# Cериализатор модели категорий
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        depth = 1
        fields = [
            'url',
            'id',
            'name',
        ]


# Cериализатор модели публикаций
class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, allow_empty=False,
                                                  label='Категория')
    image = serializers.ImageField(label='Изображение', allow_null=True, use_url=True)

    class Meta:
        model = Post
        # depth = 1
        fields = [
            'url',
            'id',
            'headline',
            'text',
            'image',
            'rating',
            'category',
            'author',
        ]

        extra_kwargs = {
            'author': {'read_only': True}
        }

    # переопредяем метод post, чтобы передать авторизованного пользователя и добавить связь со многими категориями
    def create(self, validated_data, **kwargs):
        # получаем данные публикации из валидатора
        categories = validated_data.pop('category')
        user = validated_data.pop('user')
        # headline = validated_data.pop('headline')
        # text = validated_data.pop('text')
        # image = validated_data.pop('image')
        # создаем публикацию
        post = Post.objects.create(**validated_data, author=user)
        # добавляем связи с категориями
        if categories:
            post.category.set(categories)

        return post


# Сериализатор модели отзывов
class ReviewSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), label='Публикация')
    image = serializers.URLField(label='URL изображения', allow_blank=True)

    class Meta:
        model = Review
        # depth = 1
        fields = [
            'url',
            'id',
            'headline',
            'text',
            'rating',
            'image',
            'post',
            'user',
        ]

        extra_kwargs = {
            'user': {'read_only': True}
        }

    # переопредяем метод post, чтобы передать авторизованного пользователя
    def create(self, validated_data, **kwargs):
        # получаем данные отзыва из валидатора
        user = validated_data.pop('user')
        post = validated_data.pop('post')

        if user == post.author:
            raise serializers.ValidationError('Создание отзывов к своим публикациям запрещено.')

        review = Review.objects.create(**validated_data, user=user, post=post)

        return review

    # переопределяем метод patch, чтобы выполнить проверку связи с моделью
    def update(self, instance, validated_data):
        instance.headline = validated_data.get('headline')
        instance.text = validated_data.get('text')
        instance.rating = validated_data.get('rating')
        instance.image = validated_data.get('image')
        post = validated_data.get('post')

        # если связь с моделью изменена
        if instance.post != post:
            raise serializers.ValidationError('Имеющаяся связью с моделью post не может быть изменена.')

        instance.save()

        return instance


# Сериализатор модели комментариев
class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), allow_null=True, label='Публикация')
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), allow_null=True, label='Отзыв')

    class Meta:
        model = Comment
        # depth = 1
        fields = [
            'url',
            'id',
            'text',
            'post',
            'review',
            'user',
        ]

        extra_kwargs = {
            'user': {'read_only': True}
        }

    # переопредяем метод post, чтобы передать авторизованного пользователя и выполнить проверки связей с моделями
    def create(self, validated_data, **kwargs):
        # получаем данные отзыва из валидатора
        user = validated_data.pop('user')
        text = validated_data.pop('text')
        post = validated_data.pop('post')
        review = validated_data.pop('review')

        # если не передано ни одной связи с моделью
        if not (post or review):
            raise serializers.ValidationError('Поля post и review не могут быть пустыми одновременно.')

        # если передана связь сразу на обе модели
        if post and review:
            raise serializers.ValidationError('Поля post и review не могут быть заполнены одновременно.')

        # если передана связь с моделью post, создаем комментарий к post
        if post and not review:
            comment = Comment.objects.create(text=text, user=user, post=post)
            return comment

        # если передана связь с моделью review, создаем комментарий к review
        if review and not post:
            comment = Comment.objects.create(text=text, user=user, review=review)
            return comment

    # переопределяем метод patch, чтобы выполнить проверки связей с моделями
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text')
        post = validated_data.get('post')
        review = validated_data.get('review')

        # если связь с моделью изменена
        if instance.post and instance.post != post:
            raise serializers.ValidationError('Имеющаяся связью с моделью post не может быть изменена.')

        if instance.review and instance.review != review:
            raise serializers.ValidationError('Имеющаяся связью с моделью review не может быть изменена.')

        # если передана связь сразу на обе модели
        if post and review:
            raise serializers.ValidationError('Поля post и review не могут быть заполнены одновременно.')

        instance.save()

        return instance


# Сериализатор модели голосов
class VoteSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), allow_null=True, label='Публикация')
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), allow_null=True, label='Отзыв')
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True, label='Комментарий')

    class Meta:
        model = Vote
        # depth = 1
        fields = [
            'url',
            'id',
            'value',
            'post',
            'review',
            'comment',
            'user',
        ]

        extra_kwargs = {
            'user': {'read_only': True}
        }

    # переопредяем метод post, чтобы передать авторизованного пользователя и выполнить проверки связей с моделями
    def create(self, validated_data, **kwargs):
        # получаем данные отзыва из валидатора
        value = validated_data.pop('value')
        user = validated_data.pop('user')
        post = validated_data.pop('post')
        review = validated_data.pop('review')
        comment = validated_data.pop('comment')
        vote = None

        # если не передано ни одной связи с моделью
        if not (post or review or comment):
            raise serializers.ValidationError('Поля post, review и comment не могут быть пустыми одновременно.')

        # если передана связь сразу на все модели
        if post and review and comment:
            raise serializers.ValidationError('Поля post, review и comment не могут быть заполнены одновременно.')

        # если передана связь сразу на две модели
        if post and review and not comment:
            raise serializers.ValidationError('Поля post и review не могут быть заполнены одновременно.')

        if post and comment and not review:
            raise serializers.ValidationError('Поля post и comment не могут быть заполнены одновременно.')

        if review and comment and not post:
            raise serializers.ValidationError('Поля review и comment не могут быть заполнены одновременно.')

        # если передана связь с post, проверяем есть ли голос
        if post:
            vote = Vote.objects.filter(Q(post_id=post.pk) & Q(user=user)).first()

        # если передана связь с review, проверяем есть ли голос
        if review:
            vote = Vote.objects.filter(Q(review_id=review.pk) & Q(user=user)).first()

        # если передана связь с comment, проверяем есть ли голос
        if comment:
            vote = Vote.objects.filter(Q(comment_id=comment.pk) & Q(user=user)).first()

        # если голос есть
        if vote:

            # если значение поменялось like на dislike или dislike на like, записываем новое значение
            if vote.value != value:
                vote.value = value
                vote.modified = timezone.now()
                vote.save(update_fields=['value', 'modified'])

            # значение не поменялось, удаляем голос
            else:
                vote.delete()

        # если голоса нет
        else:

            # если передана связь с post, создаем голос для post
            if post:
                vote = Vote.objects.create(user=user, post=post, value=value)

            # если передана связь с review, создаем голос для review
            if review:
                vote = Vote.objects.create(user=user, review=review, value=value)

            # если передана связь с comment, создаем голос для comment
            if comment:
                vote = Vote.objects.create(user=user, comment=comment, value=value)

        return vote

    # переопределяем метод patch, чтобы выполнить проверки связей с моделями
    # def update(self, instance, validated_data):
    #     instance.value = validated_data.get('value')
    #     post = validated_data.get('post')
    #     review = validated_data.get('review')
    #     comment = validated_data.get('comment')
    #
    #     # если связь с моделью изменена
    #     if instance.post and instance.post != post:
    #         raise serializers.ValidationError('Имеющаяся связью с моделью post не может быть изменена.')
    #
    #     if instance.review and instance.review != review:
    #         raise serializers.ValidationError('Имеющаяся связью с моделью review не может быть изменена.')
    #
    #     if instance.comment and instance.comment != comment:
    #         raise serializers.ValidationError('Имеющаяся связью с моделью comment не может быть изменена.')
    #
    #     # если передана связь сразу на все модели
    #     if post and review and comment:
    #         raise serializers.ValidationError('Поля post, review и comment не могут быть заполнены одновременно.')
    #
    #     # если передана связь сразу на две модели
    #     if post and review and not comment:
    #         raise serializers.ValidationError('Поля post и review не могут быть заполнены одновременно.')
    #
    #     if post and comment and not review:
    #         raise serializers.ValidationError('Поля post и comment не могут быть заполнены одновременно.')
    #
    #     if review and comment and not post:
    #         raise serializers.ValidationError('Поля review и comment не могут быть заполнены одновременно.')
    #
    #     instance.save()
    #
    #     return instance
