from django.db import models
from django.utils import timezone


class Code(models.Model):
    """Represent a code, which can be used to verify users."""

    # Automatically computed fields
    value = models.BigAutoField(primary_key=True, editable=False)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["timestamp"]
        indexes = [
            models.Index(fields=["timestamp"]),
        ]
