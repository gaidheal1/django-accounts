from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='users/profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
