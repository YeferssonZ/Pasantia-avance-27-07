from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index),
    path('login/', views.login, name='login'),
]