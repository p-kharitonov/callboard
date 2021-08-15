from django.contrib import admin
from django.utils.html import format_html
from .models import *


class ImageInline(admin.TabularInline):
    model = Image
    fields = ('alt', 'url', 'small_image_tag', )
    readonly_fields = ('small_image_tag',)
    extra = 1
    max_num = 8

    def small_image_tag(self, obj):
        if obj.url:
            return format_html(f'<img src="{obj.path}" style="max-height:80px; max-width:80px"')
        else:
            return ''

    small_image_tag.short_description = "Изображение"


class VideoInline(admin.TabularInline):
    model = Video
    fields = ('url',)
    extra = 1
    max_num = 8


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'is_active')
    list_filter = ('is_active', 'user__username', 'category__name',)
    search_fields = ('user', 'title', 'content',)
    fields = ('is_active', 'user', 'title', 'category', 'content', ('created_at', 'updated_at'))
    readonly_fields = ('created_at', 'updated_at',)
    list_display_links = ('id', 'title',)
    inlines = [
        ImageInline,
        VideoInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at', 'is_accept', 'is_active')
    list_filter = ('user__username', 'is_active', 'is_accept')
    search_fields = ('user', 'content',)
    field = ('is_active', 'is_accept', 'user', 'post', 'content', 'created_at')
    # readonly_fields = ('is_active', 'is_accept', 'user', 'post', 'content', 'created_at')
    readonly_fields = ('created_at',)
    list_display_links = ('id', 'post',)
