from django.urls import path, include
from tv_shows import views
from video import views as video_views

app_name = 'shows'
urlpatterns = [
    path('', views.main_shows, name='main_shows'),
    path('<slug:shows_slug>/', include(
        [
            path('detail/', views.single_shows, name='detail_shows'),
            path('season-<int:season>/episode-<int:pk_series>/', include([
                path('', views.watch_series, name='watch_series'),
                path('watch/', video_views.get_streaming_video, name='watch_shows')
            ]))
        ]
    ))
]