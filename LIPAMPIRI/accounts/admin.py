from django.contrib import admin
from .models import CustomUser, UserSettings, UserProfile, UserMembership

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserSettings)
admin.site.register(UserProfile)
admin.site.register(UserMembership)
