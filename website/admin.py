from django.contrib import admin
from .models import BlacklistItem

@admin.register(BlacklistItem)
class BlacklistItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'age_group', 'risk_level', 'updated_at')
    list_filter = ('category', 'age_group', 'risk_level')
    search_fields = ('name', 'short_description')
    ordering = ('-risk_level', 'name')
