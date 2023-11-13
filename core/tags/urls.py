from django.urls import path
from tags import views


app_name = 'tags'
urlpatterns = [
    path('<slug:tags_slug>/', views.MainGenre.as_view(), name='main_tags'),
]