from django.contrib import admin

# Register your models here.
# Teacher/admin.py

from django.contrib import admin
from .models import Mark,Assignment,Note


admin.site.register(Mark)
admin.site.register(Assignment)
admin.site.register(Note)