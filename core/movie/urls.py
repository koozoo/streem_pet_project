from django.urls import path, include
from movie import views
from video import views as video_views

app_name = 'movie'
urlpatterns = [
    path('', views.MainMovie.as_view(), name='main_movie'),
    path('<slug:movie_slug>/', include(
        [
            path('watch/', video_views.get_streaming_video, name='watch_movie'),
            path('detail/', views.single_movie, name='detail_movie')
        ]
    ))
]
