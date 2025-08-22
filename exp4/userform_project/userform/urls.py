from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_form_view, name='user_form'),
    path('users/', views.user_list_view, name='user_list'),
]