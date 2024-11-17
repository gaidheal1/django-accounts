from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='users/profile_pics/', null=True, blank=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)

    def add_xp(self, amount):
        """Add XP and handle level-up logic."""
        self.xp += amount
        while self.xp >= self.get_xp_for_next_level():
            self.level_up()
        self.save()

    def level_up(self):
        """Increase level and reset XP."""
        self.xp -= self.get_xp_for_next_level()
        self.level += 1

    def get_xp_for_next_level(self):
        return 100 * (self.level + 1) if self.level >= 1 else 100

    def __str__(self):
        return f"{self.user.username}: Level {self.level}, XP: {self.xp}"
    
    def add_activity(self, time, num):
        self.total_time += time
        self.total_activities += num
    
class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

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

        if self.user:
            self.user.profile.add_activity(self.time, 1)
            self.user.profile.save()

        if self.skill:
            self.skill.time += self.time
            self.skill.save()
        
        from users.utils import check_achievements
        new_achievements = check_achievements(self.user)

        if new_achievements:
            for achievement in new_achievements:
                print(f'You got the achievement: {achievement.name}!')
        super().save(*args, **kwargs)
    
class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    criteria = models.CharField(
        max_length=255,
        help_text="Define criteria logic in code, e.g., 'total_time >= 5'"
    )
    xp_reward = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement') # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

class GlobalStats(models.Model):
    total_time = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)

    def update_stats(self, time, num):
        """Update global time and number of activities"""
        self.total_time += time
        self.total_activities += num
        self.save()

    def __str__(self):
        return f"Total time: {self.total_time}, Total activities: {self.total_activities}"