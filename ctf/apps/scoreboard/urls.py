from django.urls import path
from . import views

app_name = 'scoreboard'

urlpatterns = [
    path('', views.scoreboard_view, name='scoreboard'),
    path('api/', views.scoreboard_api, name='api'),
]
