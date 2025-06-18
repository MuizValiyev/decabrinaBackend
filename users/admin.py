from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_staff']
    ordering = ['email']
    search_fields = ['email']
    fieldsets = (
        (None, {'fields':('email', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name')}),
        ('Personal', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
