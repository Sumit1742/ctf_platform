from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    path('', views.challenge_list, name='list'),
    path('<int:pk>/', views.challenge_detail, name='detail'),
    path('<int:pk>/submit/', views.submit_flag, name='submit'),
    path('<int:pk>/hint/<int:hint_index>/', views.unlock_hint, name='hint'),
]
