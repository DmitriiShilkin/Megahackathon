from django.contrib import admin

from .models import Post, Category, Ip, Review, Comment, Vote


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


# Register your models here.
admin.site.register(Post)
admin.site.register(Ip)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Category, CategoryAdmin)
