from django.urls import path
from .views import entry_list, entry_detail, entry_create, entry_edit, entry_delete

app_name = 'journal'

urlpatterns = [
    path('', entry_list, name='entry_list'),
    path('<int:pk>/', entry_detail, name='entry_detail'),
    path('new/', entry_create, name='entry_create'),
    path('<int:pk>/edit/', entry_edit, name='entry_edit'),
    path('<int:pk>/delete/', entry_delete, name='entry_delete'),
]

