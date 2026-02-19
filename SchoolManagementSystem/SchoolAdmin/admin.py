from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Teacher)
admin.site.register(SchoolClass)
admin.site.register(Division)
admin.site.register(Subject)
admin.site.register(TeacherAssignment)
admin.site.register(Attendance)