from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Integrate the Custom User Model into Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Show extra fields when editing an existing user
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

    # Show extra fields when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
