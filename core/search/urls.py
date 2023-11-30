from django.urls import path
from search import views

app_name = 'filter'
urlpatterns = [
    path('', views.FilterForm.as_view(), name='sort'),

]