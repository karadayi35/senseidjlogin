from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Display subscription details in the admin panel
    list_display = ['email', 'is_active', 'is_staff', 'is_subscription_active', 'subscription_end_date']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Subscription Info', {'fields': ('is_subscription_active', 'subscription_end_date')}),  # New section
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_subscription_active', 'subscription_end_date')},
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    list_filter = ('is_active', 'is_subscription_active')  # Filters for easy navigation

# Register the model with the custom admin configuration
admin.site.register(CustomUser, CustomUserAdmin)
