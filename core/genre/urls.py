from django.urls import path, include
from genre import views


app_name = 'genre'
urlpatterns = [
    path('<slug:genre_slug>/', views.listing, name='main_genre'),
]