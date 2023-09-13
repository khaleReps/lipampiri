from django.urls import path
from .views import CustomRegisterView, CustomLoginView, CustomLogoutView, ProfileView, ProfileEditView, SettingsView, SettingsEditView, DeleteProfileView,DeleteSettingsView, MembershipView, MembershipEditView, DeleteMembershipView, AccountView, SearchView

app_name = 'accounts'

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('search/', SearchView, name='search_view'),
    
    path('account/', AccountView, name='account'),
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile_edit'),
    path('delete-profile/', DeleteProfileView.as_view(), name='delete_profile'),


    path('settings/', SettingsView.as_view(), name='settings'),
    path('settings/edit/<int:pk>/', SettingsEditView.as_view(), name='settings_edit'),
    path('delete-settings/', DeleteSettingsView.as_view(), name='delete_profile'),


    path('membership/', MembershipView.as_view(), name='membership'),
    path('membership/edit/<int:pk>/', MembershipEditView.as_view(), name='membership_edit'),
    path('membership/delete/', DeleteMembershipView.as_view(), name='delete_membership'),
]
