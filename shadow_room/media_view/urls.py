from django.urls import path
from . import views

app_name = 'media_view'

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.movie_list, name='movie_list'),
    path('tv/', views.tv_list, name='tv_list'),
    path('animation', views.animation_list, name='animation_list'),
    path('animated_film/', views.animated_film_list, name='animated_film_list'),
    path('category/', views.category_list, name='category_list'),
    path('documentary/', views.documentary_list, name='documentary_list'),
    path('<int:media_id>/', views.media_detail, name='media_detail'),
]
