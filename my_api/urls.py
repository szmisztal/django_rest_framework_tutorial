from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from my_api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'movies', views.MovieViewSet, basename = 'movie')
router.register(r'reviews', views.ReviewViewSet, basename = 'review')
router.register(r'actors', views.ActorViewSet, basename = 'actor')

urlpatterns = [
    path('', include(router.urls)),
]
