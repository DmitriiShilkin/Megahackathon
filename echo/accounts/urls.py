from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from accounts import views as accounts_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', accounts_views.register, name='signup'),
    path('profile/', accounts_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='userprofile/logout.html'), name='logout'),
    path('', include('posts.urls')),
]