
# Create your models here.

from django.db import models
from django.conf import settings
from datetime import date

class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )

    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# School Class
class SchoolClass(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Division

class Division(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="divisions"
    )
    name = models.CharField(max_length=10)

    class Meta:
        unique_together = ('school_class', 'name')

    def __str__(self):
        return f"{self.school_class.name} - {self.name}"

# Subject

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    school_class = models.ForeignKey(
        'SchoolClass',
        on_delete=models.CASCADE,
        related_name='subjects'
    )

    is_practical = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'school_class')

    def __str__(self):
        return f"{self.name} ({self.school_class.name})"




# Teacher Assignment

class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('teacher', 'subject', 'division')

    def __str__(self):
        return f"{self.teacher.name} - {self.subject.name} - {self.division}"

# Student table

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=150)
    guardian_name = models.CharField(max_length=150)

    address = models.TextField()

    contact_number = models.CharField(max_length=15)

    date_of_birth = models.DateField()

    aadhar_number = models.CharField(max_length=12, unique=True)

    date_of_joining = models.DateField(default=date.today)

    division = models.ForeignKey(
        'Division',
        on_delete=models.PROTECT,
        related_name="students"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.division}"

# Attendance Model




class Attendance(models.Model):

    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    date = models.DateField(default=date.today)

    status = models.BooleanField(default=False)  # True = Present

    class Meta:
        unique_together = ('student', 'date')  # Prevent duplicate attendance

    def __str__(self):
        return f"{self.student.name} - {self.date} - {'Present' if self.status else 'Absent'}"

# --------------------
# ANNOUNCEMENTS
# --------------------
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


