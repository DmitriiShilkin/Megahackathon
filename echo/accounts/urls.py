from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from . import views
from .views import *

urlpatterns = [

    path('login/', CustomLoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='userprofile/logout.html', next_page='login'), name='logout'),
    path('signup/', RegisterPage.as_view(template_name='userprofile/signup.html'), name='signup'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='userprofile/change_password.html')),
    path('edit_user/', UserEditView.as_view(template_name='userprofile/edit_user.html'), name='edit_user'),
    path('user_profile/<int:pk>/', ShowProfilePageView.as_view(template_name='userprofile/user_profile.html'), name='user_profile'),
    path('edit_profile/<int:pk>/', EditProfilePageView.as_view(template_name='userprofile/edit_profile.html'), name='edit_profile'),
    path('create_profile/', CreateProfilePageView.as_view(template_name='userprofile/create_profile.html'), name='create_profile'),
    path('contact/', views.contact, name="contact")
]
