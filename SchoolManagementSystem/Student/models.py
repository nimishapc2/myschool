from django.db import models
from SchoolAdmin.models import Student
from Teacher.models import Assignment

# Create your models here.

from django.db import models
from django.core.validators import FileExtensionValidator

class StudentSubmission(models.Model):

    student = models.ForeignKey(
        'SchoolAdmin.Student',
        on_delete=models.CASCADE
    )

    assignment = models.ForeignKey(
        'Teacher.Assignment',
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to='submissions/',
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx']
        )]
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    # ✅ ADD THIS FIELD
    marks = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
