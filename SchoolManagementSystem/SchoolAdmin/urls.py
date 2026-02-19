"""
URL configuration for SchoolManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .import views

app_name = "SchoolAdmin" 

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_teacher/',views.add_teacher,name='add_teacher'),
    path('view-teachers/', views.view_teachers, name='view_teachers'),
    path('subject-assignments/', views.subject_assignments, name='subject_assignments'),
    path('teacher-assignments-view/', views.teacher_assignment_view, name='teacher_assignment_view'),
    path('add-student/', views.add_student, name='add_student'),
    path('view-students/', views.view_students, name='view_students'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),
    path('monthly-attendance/', views.monthly_attendance, name='monthly_attendance'),
    path('monthly-attendance/excel/', views.monthly_attendance_excel, name='monthly_attendance_excel'),
    path('add-announcement/', views.add_announcement, name='add_announcement'),
    path('announcements/', views.announcement_list, name='announcement_list'),





]
