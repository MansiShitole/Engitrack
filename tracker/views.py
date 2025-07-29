
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .models import Skill
from .forms import SkillForm, RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student,Skill
from .forms import UserUpdateForm,StudentUpdateForm
from .models import UserProfile

from .forms import ProfileImageForm
from .forms import ProfileImageForm
from django.db.models import Count
from collections import Counter
from .models import Skill

from .forms import RegisterForm
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils.dateformat import DateFormat
from django.contrib.auth.decorators import login_required








# Home View: Display all skills for the logged-in user
@login_required
def home(request):
    skills = Skill.objects.filter(user=request.user)
    category_data = skills.values('category').annotate(count=Count('id'))
    category_labels = [item['category'] for item in category_data]
    category_counts = [item['count'] for item in category_data]

    # Month-wise Skills Added
    month_data = skills.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    month_labels = [DateFormat(item['month']).format('F Y') for item in month_data]
    month_counts = [item['count'] for item in month_data]

    context = {
        'skills': skills,
        'category_labels': category_labels,
        'category_counts': category_counts,
        'month_labels': month_labels,
        'month_counts': month_counts,
    }
    return render(request, 'tracker/home.html', {'skills': skills})


# Add Skill View: Allow users to add a new skill
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, '✅ Skill added successfully!')
            return redirect('home')
    else:
        form = SkillForm()
    return render(request, 'tracker/add_skill.html', {'form': form})


# Register View: Create a new user account
from .forms import RegisterForm  # make sure this is imported

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.success(request, '✅ Account created! Please log in.')
            return redirect('login_user')
        else:
            messages.error(request, '❌ Please correct the error below.')
    else:
        form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})

# Login View: Handle user authentication
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'👋 Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, '❌ Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})



# Logout View: Log out the user
def logout_user(request):
    logout(request)
    messages.info(request, '👋 You have been logged out.')
    return redirect('login_user')

# Edit
@login_required
def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('home')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'tracker/skill_form.html', {'form': form})

# Delete
@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully!')
        return redirect('home')
    return render(request, 'tracker/skill_confirm_delete.html', {'skill': skill})

@login_required
def profile_view(request):
    profile, created= UserProfile.objects.get_or_create(user=request.user)
    skills = Skill.objects.filter(user = request.user)

    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileImageForm(instance=profile)

    return render(request, 'tracker/profile.html', {'form': form, 'user_profile': profile,'skills':skills,})
    
    

from .forms import UserUpdateForm, StudentUpdateForm

@login_required
def edit_profile(request):
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        student_form = StudentUpdateForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            return redirect('tracker/profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        student_form = StudentUpdateForm(instance=student)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'student_form': student_form,
    })

@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
    return redirect('profile')



def dashboard_view(request):
    skills = Skill.objects.filter(user=request.user).order_by('-updated_at')
    categories = [s.category for s in skills]
    most_common_category = Counter(categories).most_common(1)
    most_common = most_common_category[0][0] if most_common_category else "N/A"

    # Category data for chart
    category_counts = Counter(categories)
    category_labels = list(category_counts.keys())
    category_data = list(category_counts.values())

    # Month-wise skills added (bar chart)
    month_data = skills.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    month_labels = [DateFormat(item['month']).format('F Y') for item in month_data]
    month_counts = [item['count'] for item in month_data]

    context = {
        'skills': skills,
        'recent_skills': skills[:5],
        'most_common_category': most_common,
        'last_updated': skills[0].updated_at if skills else None,
        'category_labels': category_labels,
        'category_data': category_data,
        'month_labels': month_labels,
        'month_counts': month_counts,

    
    }
    return render(request, 'tracker/dashboard.html', context)

def about_view(request):
    return render(request, 'tracker/about.html')

from django.shortcuts import render

def register_view(request):
    return render(request, 'register.html')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Skill, Endorsement

@login_required
def endorse_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    if skill.user == request.user:
        return redirect('dashboard')  # Prevent endorsing own skill

    if not Endorsement.objects.filter(skill=skill, endorsed_by=request.user).exists():
        Endorsement.objects.create(skill=skill, endorsed_by=request.user)

    return redirect('dashboard')  # or profile view

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Skill, Endorsement
from .forms import EndorsementForm

def endorse_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    if skill.user == request.user:
        messages.error(request, "You can't endorse your own skill.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = EndorsementForm(request.POST)
        if form.is_valid():
            endorsement, created = Endorsement.objects.get_or_create(
                skill=skill,
                endorsed_by=request.user,
                defaults={'comment': form.cleaned_data['comment']}
            )
            if not created:
                messages.warning(request, "You have already endorsed this skill.")
            else:
                messages.success(request, "Endorsement submitted!")
    return redirect('dashboard')
    

def explore_skills(request):
    skills = Skill.objects.exclude(user=request.user)  # Show only others' skills
    return render(request, 'tracker/explore_skills.html', {'skills': skills})




   

