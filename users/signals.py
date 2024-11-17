from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, GlobalStats

    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a profile for the user when a new user is created"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Save the profile when the user is saved"""
    instance.profile.save()

@receiver(post_save, sender=Profile)
def update_global(sender, instance, created, **kwargs):
    if created: 
        global_stats = GlobalStats.objects.first()
        if global_stats:
            global_stats.update_stats(instance.time, instance.num)
        else:
            GlobalStats.objects.create()