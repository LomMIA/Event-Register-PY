import uuid

from django.db import models
from django.conf import settings


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликовано'
        CANCELED = 'canceled', 'Отменено'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=200, choices=Status.choices, default=Status.DRAFT)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['starts_at']

    def __str__(self):
        return self.name

class Registration(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активна'
        CHECKED_IN = 'checked_in', 'Отмечен на входе'
        CANCELED = 'canceled', 'Отменено'

    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='registrations')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    ticket_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'email'], name='unique_registration_per_event'
            )
        ]

    def __str__(self):
        return f'{self.name} — {self.event}'
