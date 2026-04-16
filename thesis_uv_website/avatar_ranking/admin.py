from django.contrib import admin
from .models import ImageRanking

@admin.register(ImageRanking)
class ImageRankingAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'ranking', 'created_at')
    list_filter = ('ranking', 'created_at')
    search_fields = ('image_name',)
    readonly_fields = ('created_at',)
    ordering = ('image_name',)
