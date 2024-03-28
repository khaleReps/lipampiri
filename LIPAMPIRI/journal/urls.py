from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntryViewSet

router = DefaultRouter()
router.register(r'entries', EntryViewSet)

app_name = 'journal'
urlpatterns = [
    path('', include(router.urls)),
]
