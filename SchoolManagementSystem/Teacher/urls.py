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
from django.urls import path, include
from .import views
urlpatterns = [
   path('my-assignments/', views.teacher_assignments, name='teacher_assignments'),
   path('add-marks/', views.add_marks, name='add_marks'),
   path('view-marks/', views.view_marks, name='view_marks'),
   path('post-assignment/', views.post_assignment, name='post_assignment'),
   path('manage-assignments/', views.manage_assignments, name='manage_assignments'),
   path('upload-notes/', views.upload_notes, name='upload_notes'),
   path('manage-notes/', views.manage_notes, name='manage_notes'),
   path('view-submission/', views.teacher_view_submission, name='teacher_view_submission'),


]
