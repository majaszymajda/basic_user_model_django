from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import Profile, User


@receiver(post_save, sender=User)
def create(sender, instance, created, **kwargs):
    """ Creates a linked Profile for User. """
    if created:
        instance.profile, _ = Profile.objects.get_or_create(user=instance)
        instance.save()
