from django.contrib import admin

from .models import Event, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'starts_at', 'location', 'capacity', 'status', 'organizer')
    list_filter = ('status', 'starts_at')
    search_fields = ('name', 'location')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'status', 'created_at')
    list_filter = ('status', 'event', 'created_at')
    search_fields = ('name', 'email', 'event__name')
    readonly_fields = ('ticket_code', 'created_at')