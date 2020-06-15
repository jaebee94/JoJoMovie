from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('list/', views.movie_list, name="movie_list"),
    # path('list/get_movies_json/<int:page>/', views.get_movies_json, name='get_movies_json')
]
