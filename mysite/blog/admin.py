from django.contrib import admin

from .models import Blog, BlogType

# 注册
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'get_read_num', 'create_time', 'last_update_time')

# @admin.register(ReadNum)
# class ReadNumAdmin(admin.ModelAdmin):
#     list_display = ('read_num', 'blog')