from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, PhotographerViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'photographers', PhotographerViewSet, basename='photographer')

urlpatterns = [
    path('', include(router.urls)),
]
