from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import PostSerializer, CategorySerializer, ReviewSerializer, CommentSerializer, VoteSerializer
from .models import Post, Category, Ip, Review, Comment, Vote
from profile.models import Profile


# Представление для категорий
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # разрешаем только перечисленные методы
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']
    # разрешено только для суперпользователя
    permission_classes = [IsAdminUser]

    # Переопределяем метод post, чтобы получить сообщения о статусе и передать контекст в сериализатор
    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request
        }
        serializer = self.get_serializer(data=request.data, context=serializer_context)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': 'OK',
                    'id': serializer.data['id']
                }
            )

        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Bad request',
                    'serializer_errors': serializer.errors,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Internal server error',
                }
            )


# Представление для публикации
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # добавляем фильтрацию записей по email пользователя и категории
    filterset_fields = ('author__username', 'category')
    # разрешаем только перечисленные методы
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    # Метод для получения айпи (нужен для определения количества просмотров)
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')  # В REMOTE_ADDR значение айпи пользователя
        return ip

    # Переопределяем метод get, чтобы сохранить ip, с которого выполняется просмотр
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        ip_req = self.get_client_ip(request)

        if instance:
            ip = Ip.objects.filter(ip=ip_req)

            if ip.exists():
                instance.views.add(ip.first())
            else:
                ip = Ip.objects.create(ip=ip_req)
                instance.views.add(ip)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Переопределяем метод post, чтобы получить сообщения о статусе, текущего пользователя и передать контекст
    # в сериализатор
    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request
        }
        serializer = self.get_serializer(data=request.data, context=serializer_context)

        if serializer.is_valid():
            # получаем текущего пользователя
            user = Profile.objects.filter(username=request.user.username)

            # если пользователь авторизован
            if user.exists():
                # передаем его в сериализатор
                serializer.save(user=user.first())
            else:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Пользователь не найден.',
                    }
                )

            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': 'OK',
                    'id': serializer.data['id']
                }
            )

        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Bad request',
                    'serializer_errors': serializer.errors,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Internal server error',
                }
            )

    # Переопределяем метод patch, чтобы проверить текущего пользователя и сохранить дату изменения
    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()

        # если текущий пользователь - автор публикации
        if request.user == post.author:
            post.modified = timezone.now()
            serializer = self.get_serializer(post, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    # {
                    #     'state': '1',
                    #     'message': 'Изменения успешно внесены.'
                    # }
                    data=serializer.data,
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        # 'state': '0',
                        'message': serializer.errors
                    }
                )
        else:
            return Response(
                {
                    # 'state': '0',
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.'
                }
            )

    # Переопределяем метод delete, чтобы проверить текущего пользователя
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()

        # если текущий пользователь - хозяин профиля
        if request.user == post.author:
            self.perform_destroy(post)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.',
                }
            )


# Представление для отзывов
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    # разрешаем только перечисленные методы
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    # Переопределяем метод post, чтобы получить сообщения о статусе, текущего пользователя и передать контекст
    # в сериализатор
    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request
        }
        serializer = self.get_serializer(data=request.data, context=serializer_context)

        if serializer.is_valid():
            # получаем текущего пользователя
            user = Profile.objects.filter(username=request.user.username)

            # если пользователь авторизован
            if user.exists():
                # передаем его в сериализатор
                serializer.save(user=user.first())

            else:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Пользователь не найден.',
                    }
                )

            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': 'OK',
                    'id': serializer.data['id']
                }
            )

        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Bad request',
                    'serializer_errors': serializer.errors,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Internal server error',
                }
            )

    # Переопределяем метод patch, чтобы проверить текущего пользователя и сохранить дату изменения
    def partial_update(self, request, *args, **kwargs):
        review = self.get_object()

        # если текущий пользователь - автор отзыва
        if request.user == review.user:
            review.modified = timezone.now()
            serializer = self.get_serializer(review, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    # {
                    #     'state': '1',
                    #     'message': 'Изменения успешно внесены.',
                    # }
                    data=serializer.data,
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        # 'state': '0',
                        'message': serializer.errors
                    }
                )
        else:
            return Response(
                {
                    # 'state': '0',
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.'
                }
            )

    # Переопределяем метод delete, чтобы проверить текущего пользователя
    def destroy(self, request, *args, **kwargs):
        review = self.get_object()

        # если текущий пользователь - хозяин профиля
        if request.user == review.user:
            self.perform_destroy(review)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.',
                }
            )


# Представление для комментариев
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    # разрешаем только перечисленные методы
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    # Переопределяем метод post, чтобы получить сообщения о статусе, текущего пользователя и передать контекст
    # в сериализатор
    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request
        }
        serializer = self.get_serializer(data=request.data, context=serializer_context)

        if serializer.is_valid():
            # получаем текущего пользователя
            user = Profile.objects.filter(username=request.user.username)

            # если пользователь авторизован
            if user.exists():
                # передаем его в сериализатор
                serializer.save(user=user.first())
            else:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Пользователь не найден.',
                    }
                )

            return Response(
                {
                    'status': status.HTTP_201_CREATED,
                    'message': 'OK',
                    'id': serializer.data['id']
                }
            )

        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Bad request',
                    'serializer_errors': serializer.errors,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Internal server error',
                }
            )

    # Переопределяем метод patch, чтобы проверить текущего пользователя и сохранить дату изменения
    def partial_update(self, request, *args, **kwargs):
        comment = self.get_object()

        # если текущий пользователь - автор комментария
        if request.user == comment.user:
            comment.modified = timezone.now()
            serializer = self.get_serializer(comment, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    # {
                    #     'state': '1',
                    #     'message': 'Изменения успешно внесены.'
                    # }
                    data=serializer.data,
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        # 'state': '0',
                        'message': serializer.errors
                    }
                )
        else:
            return Response(
                {
                    # 'state': '0',
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.'
                }
            )

    # Переопределяем метод delete, чтобы проверить текущего пользователя
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()

        # если текущий пользователь - хозяин профиля
        if request.user == comment.user:
            self.perform_destroy(comment)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.',
                }
            )


# Представление для голосов
class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
    # разрешаем только перечисленные методы
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request
        }
        serializer = self.get_serializer(data=request.data, context=serializer_context)

        if serializer.is_valid():
            # получаем текущего пользователя
            user = Profile.objects.filter(username=request.user.username)

            # если пользователь авторизован
            if user.exists():
                serializer.save(user=user.first())
            else:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Пользователь не найден.',
                    }
                )

            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'OK',
                    'id': serializer.data['id'],
                }
            )

        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Bad request',
                    'serializer_errors': serializer.errors,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Internal server error',
                }
            )
