

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver  
from datetime import date 
from django.db import models
from django.contrib.auth.models import User



class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Technical', 'Technical'),
        ('Soft Skill', 'Soft Skill'),
        ('Certification', 'Certification'),
        ('Project', 'Project'),
        ('Other', 'Other'),
    ]

    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    goal_date = models.DateField(null=True, blank=True)  # NEW
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)  

    def days_remaining(self):
        if self.goal_date:
            delta = (self.goal_date - date.today()).days
            return max(delta, 0)
        return None


    def __str__(self):
        return f"{self.name} ({self.level})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.jpg')

    def __str__(self):
        return self.user.username



class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('cert', 'Certification'),
        ('comp', 'Competition'),
        ('intern', 'Internship'),
        ('award', 'Award'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date_earned = models.DateField()
    certificate = models.FileField(upload_to='achievement_docs/', blank=True, null=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    

from django.db import models
from django.contrib.auth.models import User

class Endorsement(models.Model):
    skill = models.ForeignKey('Skill', related_name='endorsements', on_delete=models.CASCADE)
    endorsed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    endorsed_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)



    class Meta:
        unique_together = ('skill', 'endorsed_by')  # prevent multiple endorsements

    def __str__(self):
        return f"{self.endorsed_by.username} endorsed {self.skill.name}"

