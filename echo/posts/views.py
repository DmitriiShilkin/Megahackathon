import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import PostSerializer, CategorySerializer
from .models import Post, Category
from sign.models import User


# представление для категорий
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# представление для публикации
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # добавляем фильтрацию записей по email пользователя и категории
    filterset_fields = ('author__user__username', 'category')
    # разрешаем только перечисленные методы
    http_method_names = ['get', 'post', 'head', 'patch', 'options', 'delete']

    # переопределяем метод post, чтобы получить сообщения о статусе и текущего пользователя
    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            # получаем текущего авторизованного пользователя и передаем его для сериализации
            user = User.objects.filter(user__username=request.user.username)

            if user.exists():
                serializer.save(user=user.first())
            else:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Пользователь не найден',
                        'id': None
                    }
                )

            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'OK',
                    'id': serializer.data['id']
                }
            )

        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Bad request',
                    'id': None,
                    'serializer_errors': serializer.errors,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Internal server error',
                    'id': None,
                }
            )

    # переопределяем метод patch
    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()

        if request.user == post.author__user:
            post.modified = datetime.datetime.now()
            serializer = PostSerializer(post, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'state': '1',
                        'message': 'Изменения успешно внесены'
                    }
                )
            else:
                return Response(
                    {
                        'state': '0',
                        'message': serializer.errors
                    }
                )
        else:
            return Response(
                {
                    'state': '0',
                    'message': 'В изменении отказано'
                }
            )
