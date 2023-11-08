from django.urls import path, include
from tv_shows import views
from video import views as video_views

app_name = 'shows'
urlpatterns = [
    path('', views.MainShows.as_view(), name='main_genre'),
]