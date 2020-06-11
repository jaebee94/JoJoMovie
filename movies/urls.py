from django.contrib import admin
from . import views

app_name = 'movies'

urlpatterns = [
    path('search/', views.search, name='search'),
]
