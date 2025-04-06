from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Automatically create a profile for the new user
        Profile.objects.get_or_create(user=instance)

        # Assign the user to a group based on their role (but exclude "admin")
        if instance.profile.role == 'customer':
            group, _ = Group.objects.get_or_create(name='Customer')
            instance.groups.add(group)
        elif instance.profile.role == 'author':
            group, _ = Group.objects.get_or_create(name='Author')
