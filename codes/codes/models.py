import binascii
import os

from django.db import models
from django.utils import timezone


class Code(models.Model):
    """Represent a code, which can be used to verify users."""

    # Automatically computed fields
    value = models.CharField(max_length=40, primary_key=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["timestamp"]
        indexes = [
            models.Index(fields=["timestamp"]),
        ]

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = binascii.hexlify(os.urandom(20)).decode()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.value
