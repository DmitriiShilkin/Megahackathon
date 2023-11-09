from django.contrib import admin

from .models import Post, Category
from sign.models import User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


# Register your models here.
admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User)
