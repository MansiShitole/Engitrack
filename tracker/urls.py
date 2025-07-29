
from django.urls import path
from . import views
from .views import profile_view



urlpatterns = [
    path('', views.home, name='home'),  
    path('add/', views.add_skill, name='add_skill'), 
    path('profile/', views.profile_view, name='profile'),
     

    # Authentication routes
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    
    #path('skill/delete/<int:pk>/', views.delete_skill, name='skill_delete'),
    path('edit-skill/<int:pk>/', views.edit_skill, name='edit_skill'), 
    path('delete-skill/<int:pk>/', views.delete_skill, name='delete_skill'),  

    path('profile/',profile_view, name='profile'),
    path('upload/', views.upload_profile_image, name='upload_profile_image'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    
    path('add-skill/', views.add_skill, name='add-skill'),
    path('edit-skill/<int:pk>/', views.edit_skill, name='edit_skill'), 
    path('delete-skill/<int:pk>/', views.delete_skill, name='delete_skill'),  
    path('about/', views.about_view, name='about'),
    path('register/',views.register_user, name='register_user'),

    path('about/', views.about_view, name='about'),
    path('endorse/<int:skill_id>/', views.endorse_skill, name='endorse_skill'),
 path('endorse/<int:skill_id>/', views.endorse_skill, name='endorse_skill'),
 path('explore/', views.explore_skills, name='explore_skills'),

]

    
    



     



