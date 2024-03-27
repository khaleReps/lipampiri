from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogBookViewSet

router = DefaultRouter()
router.register(r'logbooks', LogBookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
