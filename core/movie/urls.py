from django.urls import path, include
from movie import views
from video import views as video_views

app_name = 'movie'
urlpatterns = [
    path('', views.main_movie, name='main_movie'),
    path('<slug:movie_slug>', include(
        [
            path('watch/', video_views.show_video, name='watch'),
            path('detail/', video_views.detail_video, name='detail_video')
        ]
    ))
]
