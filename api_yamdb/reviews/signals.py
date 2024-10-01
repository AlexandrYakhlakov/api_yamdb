from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save(instance, created, **kwargs):
    if created:
        confirmation_code = '1235'
        instance.confirmation_code = confirmation_code
        instance.save()
