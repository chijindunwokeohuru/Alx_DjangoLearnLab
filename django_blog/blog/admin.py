from django.contrib import admin
from .models import Post, Comment, Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    list_filter = ['published_date', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'title': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ['-published_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content']
    ordering = ['-created_at']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__username', 'bio']
