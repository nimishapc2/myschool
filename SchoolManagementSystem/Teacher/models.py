from django.db import models
from SchoolAdmin.models import Student,Subject,Teacher
# Create your models here.

    
#Mark Model

class Mark(models.Model):

    EXAM_TYPES = (
        ('FIRST_MID', 'First Mid Term'),
        ('FIRST_TERM', 'First Term'),
        ('SECOND_MID', 'Second Mid Term'),
        ('ANNUAL', 'Annual Exam'),
    )

    student = models.ForeignKey(
        'SchoolAdmin.Student',
        on_delete=models.CASCADE,
        related_name="marks"
    )

    subject = models.ForeignKey(
        'SchoolAdmin.Subject',
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        'SchoolAdmin.Teacher',
        on_delete=models.CASCADE
    )

    exam = models.CharField(
        max_length=20,
        choices=EXAM_TYPES
    )

    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'exam')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.get_exam_display()}"

# Assignment
class Assignment(models.Model):

    teacher = models.ForeignKey(
        'SchoolAdmin.Teacher',
        on_delete=models.CASCADE
    )

    school_class = models.ForeignKey(
        'SchoolAdmin.SchoolClass',
        on_delete=models.CASCADE
    )

    division = models.ForeignKey(
        'SchoolAdmin.Division',
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        'SchoolAdmin.Subject',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    due_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.division}"
    
    

# Notes
from django.core.validators import FileExtensionValidator

class Note(models.Model):

    teacher = models.ForeignKey(
        'SchoolAdmin.Teacher',
        on_delete=models.CASCADE
    )

    school_class = models.ForeignKey(
        'SchoolAdmin.SchoolClass',
        on_delete=models.CASCADE
    )

    division = models.ForeignKey(
        'SchoolAdmin.Division',
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        'SchoolAdmin.Subject',
        on_delete=models.CASCADE
    )

    lesson_number = models.CharField(max_length=50)

    title = models.CharField(max_length=200)

    file = models.FileField(
        upload_to='notes/',
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx']
        )]
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subject.name}"
