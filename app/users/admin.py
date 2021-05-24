from .models import User, YahooAccount
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

# Register your models here.

@admin.register(User)
class AdminUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('account_id', 'password','plan')}),
        (_('Personal info'), {'fields': ('full_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       )})
    )
    list_display = ('account_id', 'email', 'full_name', 'plan', 'is_staff')
    list_filter = []
    search_fields = ('account_id', 'full_name', 'email')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_id', 'password1', 'password2'),
        }),
    )
    ordering = ('account_id',)