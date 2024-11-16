from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='users/profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
# class Task(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    time = models.IntegerField(default=0)
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created'] # Most recent activities first
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Add the activity duration to the skill's total_time when saving the activity
        if self.pk:
            old_activity = Activity.objects.get(pk=self.pk)
            if old_activity.skill:
                old_activity.skill.time -= old_activity.time
                old_activity.skill.save()

        if self.skill:
            self.skill.time += self.time
            self.skill.save()
        super().save(*args, **kwargs)
    
