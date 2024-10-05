import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def post_save(instance, created, **kwargs):
    if created:
        confirmation_code = uuid.uuid4().hex
        instance.confirmation_code = confirmation_code
        instance.save()
