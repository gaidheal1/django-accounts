from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Activity, Skill


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'time', 'skill']
        widgets = {
            'skill': forms.Select(attrs={'required': False}) # Optional skill
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['skill'].queryset = Skill.objects.filter(user=user)