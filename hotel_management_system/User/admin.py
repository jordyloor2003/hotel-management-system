from django.contrib import admin
from .models import User

def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)

deactivate_users.short_description = "Deactivate selected users"

def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)

activate_users.short_description = "Reactivate selected users"

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_hotel_owner', 'is_customer', 'is_superuser', 'groups')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_hotel_owner', 'is_customer', 'is_superuser', 'is_active')
    actions = [deactivate_users, activate_users]

    def groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    groups.short_description = 'Groups'

admin.site.register(User, UserAdmin)