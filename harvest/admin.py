from django.contrib import admin
from .models import Dataset

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'theme', 'publication_date')
    search_fields = ('title', 'source', 'keywords')
