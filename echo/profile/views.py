# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

# from . import forms
# from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from .models import Profile
from .serializers import ProfileSerializer


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'userprofile/signup.html', {'form': form})
#
#
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST,
#                                    request.FILES,
#                                    instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Ваш профиль успешно обновлен.')
#             return redirect('profile')
#
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }
#
#     return render(request, 'userprofile/profile.html', context)
#
#
# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name']
#
#
# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image', 'bio', 'vk', 'telegram', 'whatsup', 'facebook', 'twitter', 'instagram']


# Представление для пользователя
# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     # разрешаем только перечисленные методы
#     http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


# Представление для профиля пользователя
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    # разрешаем только перечисленные методы
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    # Переопределяем метод get, чтобы выполнить проверку пользователя
    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()

        # если текущий пользователь - хозяин профиля или админ
        if request.user == profile or request.user.is_staff:
            serializer = self.get_serializer(profile)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.',
                }
            )

    # Переопределяем метод get_list, чтобы выполнить проверку пользователя
    def list(self, request, *args, **kwargs):
        # Если текущий пользователь - админ
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        else:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.',
                }
            )

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

    # Переопределяем метод patch, чтобы проверить текущего пользователя
    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()

        # если текущий пользователь - хозяин профиля
        if request.user == profile:
            serializer = self.get_serializer(profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    # {
                    #     'state': '1',
                    #     'message': 'Изменения успешно внесены.',
                    # },
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
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.'
                }
            )

    # Переопределяем метод delete, чтобы проверить текущего пользователя
    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()

        # если текущий пользователь - хозяин профиля
        if request.user == profile:
            self.perform_destroy(profile)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(
                {
                    'status': status.HTTP_403_FORBIDDEN,
                    'message': 'Действие запрещено.',
                }
            )
