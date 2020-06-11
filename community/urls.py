from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:review_pk>/', views.detail, name='detail'),
    path('<int:review_pk>/update/', views.update, name='update'),
    path('<int:review_pk>/delete/', views.delete, name='delete'),
    path('<int:review_pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:review_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, 
    name='comment_delete'),
    path('<int:review_pk>/comment/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
]