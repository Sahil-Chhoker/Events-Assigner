from django.db import models
from django.core.validators import MinValueValidator


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    photographers_required = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_name} on {self.event_date}"


class Photographer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Assignment(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    photographer = models.ForeignKey(
        Photographer,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    class Meta:
        unique_together = ['event', 'photographer']
        ordering = ['event', 'photographer']

    def __str__(self):
        return f"{self.photographer.name} assigned to {self.event.event_name}"
