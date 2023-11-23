from rest_framework import serializers

from .models import Profile
from posts.models import Post, Category


# Сериализатор модели профиля пользователя
class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, label='Пароль', write_only=True)
    favourite = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True,
                                                   label='Избранные публикации')
    subscribed_categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True,
                                                               label='Подписки на категории')
    subscribed_users = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=True,
                                                          label='Подписки на пользователей')
    image = serializers.URLField(label='URL фотографии', allow_blank=True)
    hide_email = serializers.BooleanField(initial=True, label='Скрыть email')

    class Meta:
        model = Profile
        fields = [
            'url',
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'city',
            'date_of_birth',
            'hide_email',
            'bio',
            'image',
            'vk',
            'telegram',
            'whatsapp',
            'facebook',
            'twitter',
            'instagram',
            'favourite',
            'subscribed_categories',
            'subscribed_users',
        ]

    # переопредяем метод post, чтобы выполнить проверки уникальности имен и почты
    def create(self, validated_data, **kwargs):
        # получаем данные профиля из валидатора
        favourite = validated_data.pop('favourite')
        subscribed_categories = validated_data.pop('subscribed_categories')
        subscribed_users = validated_data.pop('subscribed_users')
        password = validated_data.pop('password')

        profile = Profile.objects.create(**validated_data)
        profile.set_password(password)
        profile.save()

        # добавляем связи с избранным
        if favourite:
            profile.favourite.set(favourite)

        # добавляем связи с подписками на категории
        if subscribed_categories:
            profile.subscribed_categories.set(subscribed_categories)

        # добавляем связи с подписками на пользователей
        if subscribed_users:
            profile.subscribed_users.set(subscribed_users)

        return profile

    # переопределяем метод patch, чтобы выполнить шифрование пароля, если он изменен
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.city = validated_data.get('city', instance.city)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.hide_email = validated_data.get('hide_email', instance.hide_email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.vk = validated_data.get('vk', instance.vk)
        instance.telegram = validated_data.get('telegram', instance.telegram)
        instance.whatsapp = validated_data.get('whatsapp', instance.whatsapp)
        instance.facebook = validated_data.get('facebook', instance.facebook)
        instance.twitter = validated_data.get('twitter', instance.twitter)
        instance.instagram = validated_data.get('instagram', instance.instagram)
        favourite = validated_data.get('favourite')
        subscribed_categories = validated_data.get('subscribed_categories')
        subscribed_users = validated_data.get('subscribed_users')
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        # если имя пользователя было изменено
        if instance.username != username:
            raise serializers.ValidationError('Имя пользователя не может быть изменено.')

        # если почта была изменена
        if instance.email != email:
            raise serializers.ValidationError('Email не может быть изменен.')

        # если пароль был изменен
        if instance.password != password:
            instance.set_password(password)

        instance.save()

        # меняем связи с избранным, если содержимое изменилось
        if favourite != instance.favourite:
            # добавляем, если значения не пустые
            if favourite:
                instance.favourite.set(favourite)
            # очищаем, если значения пустые
            else:
                instance.favourite.clear()

        # меняем связи с подписками на категории, если содержимое изменилось
        if subscribed_categories != instance.subscribed_categories:
            # добавляем, если значения не пустые
            if subscribed_categories:
                instance.subscribed_categories.set(subscribed_categories)
            # очищаем, если значения пустые
            else:
                instance.subscribed_categories.clear()

        # меняем связи с подписками на пользователей, если содержимое изменилось
        if subscribed_users != instance.subscribed_users:
            # добавляем, если значения не пустые
            if subscribed_users:
                instance.subscribed_users.set(subscribed_users)
            # очищаем, если значения пустые
            else:
                instance.subscribed_users.clear()

        return instance
