import binascii
import os

from django.db import models, IntegrityError
from django.utils import timezone


class CodeManager(models.Manager):
    def create(self, *args, **kwargs):
        """
        Provide a convenience wrapper for the creation of codes.

        Since the value of a code is generated randomly, it is
        very rare but possible, that the value already exists.

        The probability for a collision is 1 / pow(16, 20),
        which computes to approx. 8 * pow(10, -25).

        Note, that the probability increases with an
        increasing number of codes, but will never
        reach an insufficiently big number.

        If two codes collide, the django ORM throws an
        IntegrityError. If the IntegrityError is thrown,
        simply try again.

        The console should be monitored every once in a while
        to ensure, that nothing else triggers IntegrityErrors.
        """
        while True:
            try:
                return super().create(*args, **kwargs)
            except IntegrityError as e:
                print(e)


class Code(models.Model):
    """Represent a code, which can be used to verify users."""

    # Automatically computed fields
    value = models.CharField(max_length=6, primary_key=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

    objects = CodeManager()

    class Meta:
        ordering = ["timestamp"]
        indexes = [
            models.Index(fields=["timestamp"]),
        ]

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = binascii.hexlify(os.urandom(20)).decode()[:6]
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.value
