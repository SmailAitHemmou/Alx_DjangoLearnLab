from django.contrib import admin
from .models import Post, Profile, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('author',)
    
admin.site.register(Profile)
admin.site.register(Comment)