from django import forms
from .models import Skill
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student
from .models import UserProfile
from django import forms



# Custom registration form using built-in UserCreationForm for password validation
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


# Form for adding/editing skills
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'level', 'description','certificate','goal_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter skill name'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of your skill'
            }),
            'certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'goal_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_pic']


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'id': 'id_profile_pic'})
        }
from django import forms
from .models import Endorsement

class EndorsementForm(forms.ModelForm):
    class Meta:
        model = Endorsement
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write a short note (optional)...',
                'class': 'form-control'
            }),
        }
