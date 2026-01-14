from django.contrib import admin
from .models import Semester, Course, ClassSession,FileCategory

# Register your models here.
admin.site.register(ClassSession)
admin.site.register(Course)
admin.site.register(FileCategory)