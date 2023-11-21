from django.urls import path

from echo.profile import views

urlpatterns = [
    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('author/', views.AuthorView.as_view({'get': 'list'})),
    path('author/<int:pk>/', views.AuthorView.as_view({'get': 'retrieve'})),

]