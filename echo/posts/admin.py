from django.contrib import admin

from .models import Post, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


# Register your models here.
admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
