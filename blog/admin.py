from django.contrib import admin
from .models import Post, BlogHead, SendMail, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(BlogHead)
class BlogHeadAdmin(admin.ModelAdmin):
    list_display=['head_title', 'head_descr']

@admin.register(SendMail)
class SendMailAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'to', 'comments']
    list_filter = ['name', 'email']
    
@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['nom', 'email', 'commentaire']