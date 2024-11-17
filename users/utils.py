from .models import Achievement, UserAchievement

def check_achievements(user):
    # Fetch all achievements
    achievements = Achievement.objects.all()
    unlocked_achievements = []

    for achievement in achievements:
        # Example: Hardcode or dynamically evaluate criteria
        if achievement.criteria == "total_time >= 300" and user.profile.total_time >= 300:
            # Check if the user already has the achievement
            if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
                # Unlock the achievement
                UserAchievement.objects.create(user=user, achievement=achievement)
                unlocked_achievements.append(achievement)
                user.profile.xp += achievement.xp_reward
                user.profile.save()

    return unlocked_achievements
