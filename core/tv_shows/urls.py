from django.urls import path, include
from tv_shows import views
from video import views as video_views

app_name = 'shows'
urlpatterns = [
    path('', views.main_shows, name='main_shows'),
    path('<slug:shows_slug>', include(
        [
            path('watch/', video_views.show_video, name='watch'),
            path('detail/', video_views.detail_video, name='detail_video')
        ]
    ))
]