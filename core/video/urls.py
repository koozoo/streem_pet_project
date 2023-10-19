from django.urls import path, include
from video import views

app_name = 'watch'
urlpatterns = [
    path('movie/', views.main_movie, name='movie'),
    path('tv_shows/', views.main_show, name='tv_shows'),
    path('tv_shows/<slug:video_slug>', include(
        [
            path('show/', views.show_video, name='show'),
            path('detail/', views.detail_video, name='detail_video')
        ]
    ))
]
