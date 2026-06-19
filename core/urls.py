"""URL-маршруты приложения core."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('booking/', views.booking, name='booking'),
    path('feedback/', views.feedback, name='feedback'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('about/', views.about, name='about'),
]
