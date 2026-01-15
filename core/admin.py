from django.contrib import admin
from .models import Semester, Course, ClassSession,FileCategory, User

# Register your models here.
admin.site.register(ClassSession)
admin.site.register(Course)
admin.site.register(FileCategory)
admin.site.register(Semester)
admin.site.register(User)