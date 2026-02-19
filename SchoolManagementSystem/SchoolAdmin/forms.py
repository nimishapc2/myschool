from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from django import forms
from SchoolAdmin.models import Teacher, Student

class TeacherCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


from django.core.exceptions import ValidationError
import re

class TeacherProfileForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ['name', 'contact_number', 'qualification', 'subject', 'address']

    def clean_contact_number(self):
        contact = self.cleaned_data.get("contact_number")

        if not re.fullmatch(r'\d{10}', contact):
            raise ValidationError("Contact number must be exactly 10 digits.")

        return contact





class StudentCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']




class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'created_at']
