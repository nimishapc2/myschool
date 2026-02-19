from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from django import forms
from SchoolAdmin.models import Teacher, Student

class TeacherCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'address', 'contact_number', 'qualification', 'subject']




class StudentCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']




class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'created_at']
