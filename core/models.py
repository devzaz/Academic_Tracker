from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)

    university = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    dob = models.DateField(
        blank=True,
        null=True
    )

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    



class Semester(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete  = models.CASCADE,
        related_name = 'semesters'
    )
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active  = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name
        
class Course(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'courses'
    )
    semester = models.ForeignKey(
        Semester,
        on_delete = models.CASCADE,
        related_name = 'courses'
    )

    name = models.CharField(max_length=150)
    course_code = models.CharField(max_length=50)
    teacher_name = models.CharField(max_length=150)
    total_class_planned = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['course_code']

    def __str__(self):
        return self.name
    


class ClassSession(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Attended'),
        ('absent', 'Absent'),
        ('cancelled', 'Cancelled'),
        ('no_attendance', 'No Attendance Taken'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='class_sessions'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    date = models.DateField()
    start_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('course', 'date', 'start_time')

    def __str__(self):
        return f"{self.course.name} - {self.date} {self.start_time}"
    

class CourseMark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='marks'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='mark'
    )

    mid1 = models.FloatField(default=0)
    mid2 = models.FloatField(default=0)
    presentation = models.FloatField(null=True, blank=True)
    assignment = models.FloatField(null=True, blank=True)
    final = models.FloatField(default=0)

    total = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        components = [
            self.mid1 or 0,
            self.mid2 or 0,
            self.final or 0
        ]

        if self.presentation is not None:
            components.append(self.presentation)

        if self.assignment is not None:
            components.append(self.assignment)

        self.total = sum(components)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.name} - Marks"


class FileCategory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'file_categories'
    )

    name = models.CharField(max_length=100)



    def __str__(self):
        return self.name
    


class Folder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'folders'
    )

    category = models.ForeignKey(
        FileCategory,
        on_delete = models.CASCADE,
        related_name = 'folders'
    )

    name = models.CharField(max_length=150)

    is_protected = models.BooleanField(default=False)
    pin_has = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return f"{self.category.name} / {self.name}"
    
    def total_size(self):
        return sum(f.size for f in self.files.all())
    






class StoredFile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stored_files"
    )

    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    file = models.FileField(upload_to="media/")
    original_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True)
    size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name or self.original_name

    


def get_general_category(user):
    return FileCategory.objects.get_or_create(
        user=user,
        name="General"
    )[0]



class Assessment(models.Model):
    TYPE_CHOICES = [
        ('mid1', 'Mid 1'),
        ('mid2', 'Mid 2'),
        ('final', 'Final Exam'),
        ('presentation', 'Presentation'),
        ('assignment', 'Assignment'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assessments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assessments'
    )

    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.name} - {self.title}"



class CalendarEvent(models.Model):
    EVENT_TYPES = [
        ('holiday', 'Holiday'),
        ('event', 'Event'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calendar_events',
        null=True,
        blank=True
    )
    # user = NULL → global event

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    is_global = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
