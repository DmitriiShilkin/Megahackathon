from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile


class ProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff',)
    search_fields = ('email', 'username',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ('is_admin',)
    fieldsets = (
                (None, {'fields': ('email', 'password')}),
                ('Персональные данные', {'fields': ('first_name', 'last_name')}),
                ('Разрешения', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
    )


admin.site.register(Profile, ProfileAdmin)
