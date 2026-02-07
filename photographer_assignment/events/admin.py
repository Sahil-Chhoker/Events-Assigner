from django.contrib import admin
from .models import Event, Photographer, Assignment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_date', 'photographers_required', 'created_at']
    list_filter = ['event_date', 'created_at']
    search_fields = ['event_name']


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'email']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['event', 'photographer']
    list_filter = ['event__event_date']
    search_fields = ['event__event_name', 'photographer__name']
