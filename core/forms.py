from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Semester, 
    Course, 
    ClassSession, 
    CourseMark, 
    StoredFile, 
    Folder, 
    FileCategory,
    Assessment,
    CalendarEvent,
    User
)





BASE_INPUT_CLASSES = (
    "w-full px-3 py-2 rounded-md "
    "border border-gray-300 "
    "bg-white text-black "
    "focus:outline-none focus:ring-2 focus:ring-blue-500"
)

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'e.g. Semester 1'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASSES
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASSES
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600'
            }),
        }




# BASE_INPUT_CLASSES = (
#     "w-full px-3 py-2 rounded-md "
#     "border border-gray-300 "
#     "bg-white text-black "
#     "focus:outline-none focus:ring-2 focus:ring-blue-500"
# )

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'semester',
            'name',
            'course_code',
            'teacher_name',
            'total_class_planned'
        ]
        widgets = {
            'semester': forms.Select(attrs={
                'class': BASE_INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'e.g. Data Structures'
            }),
            'course_code': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'e.g. CS201'
            }),
            'teacher_name': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'e.g. Dr. Smith'
            }),
            'total_class_planned': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'min': 1
            }),
        }





# BASE_INPUT_CLASSES = (
#     "w-full px-3 py-2 rounded-md "
#     "border border-gray-300 "
#     "bg-white text-black "
#     "focus:outline-none focus:ring-2 focus:ring-blue-500"
# )

class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = ['course', 'date', 'start_time']
        widgets = {
            'course': forms.Select(attrs={
                'class': BASE_INPUT_CLASSES
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASSES
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': BASE_INPUT_CLASSES
            }),
        }


# BASE_INPUT_CLASSES = (
#     "w-full px-3 py-2 rounded-md "
#     "border border-gray-300 "
#     "bg-white text-black "
#     "focus:outline-none focus:ring-2 focus:ring-blue-500"
# )

class CourseMarkForm(forms.ModelForm):
    class Meta:
        model = CourseMark
        fields = ['mid1', 'mid2', 'presentation', 'assignment', 'final']
        widgets = {
            'mid1': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'min': 0
            }),
            'mid2': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'min': 0
            }),
            'presentation': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'min': 0
            }),
            'assignment': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'min': 0
            }),
            'final': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'min': 0
            }),
        }



# BASE_INPUT_CLASSES = (
#     "w-full px-3 py-2 rounded-md "
#     "border border-gray-300 "
#     "bg-white text-black "
#     "focus:outline-none focus:ring-2 focus:ring-blue-500"
# )

class FileUploadForm(forms.ModelForm):
    display_name = forms.CharField(
        required=False,
        label="File name (optional)"
    )
    class Meta:
        model = StoredFile
        fields = ["folder", "course",'display_name', "file"]
        widgets = {
            "folder": forms.Select(attrs={
                "class": BASE_INPUT_CLASSES
            }),
            "course": forms.Select(attrs={
                "class": BASE_INPUT_CLASSES
            }),
            "file": forms.ClearableFileInput(attrs={
                "class": "w-full text-black bg-white border border-gray-300 rounded-md"
            }),
        }


class FolderForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ["category", "name"]
        widgets = {
            "category": forms.Select(attrs={
                "class": BASE_INPUT_CLASSES
            }),
            "name": forms.TextInput(attrs={
                "class": BASE_INPUT_CLASSES,
                "placeholder": "e.g. Lecture Notes"
            }),
        }


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ["name", "category"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 rounded-lg bg-gray-900 border border-gray-700 text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            "category": forms.Select(attrs={
                "class": "w-full px-3 py-2 rounded-lg bg-gray-900 border border-gray-700 text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
        }




# BASE_INPUT_CLASSES = (
#     "w-full px-3 py-2 rounded-md "
#     "border border-gray-300 "
#     "bg-white text-black "
#     "focus:outline-none focus:ring-2 focus:ring-blue-500"
# )

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['course', 'title', 'type', 'date']
        widgets = {
            'course': forms.Select(attrs={
                'class': BASE_INPUT_CLASSES
            }),
            'title': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'e.g. Midterm Exam'
            }),
            'type': forms.Select(attrs={
                'class': BASE_INPUT_CLASSES
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASSES
            }),
        }


class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'event_type', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'e.g. Mid Term Break'
            }),
            'event_type': forms.Select(attrs={
                'class': BASE_INPUT_CLASSES
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASSES
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASSES
            }),
        }


class SignupForm(UserCreationForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600'
        })
    )

    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'full_name',
            'mobile',
            'university',
            'dob',
            'password1',
            'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'university': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-900 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
        }
# class SignupForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'email',
#             'full_name',
#             'mobile',
#             'university',
#             'dob',
#             'password1',
#             'password2'
#         ]
#         widgets = {
#             'dob': forms.DateInput(attrs={'type': 'date'})
#         }



# class CalendarEventForm(forms.ModelForm):
#     class Meta:
#         model = CalendarEvent
#         fields = ['title', 'event_type', 'start_date', 'end_date']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#             'end_date': forms.DateInput(attrs={'type': 'date'}),
#         }


# class AssessmentForm(forms.ModelForm):
#     class Meta:
#         model = Assessment
#         fields = ['course', 'title', 'type', 'date']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'})
#         }



# class FolderForm(forms.ModelForm):
#     class Meta:
#         model = Folder
#         fields = ["name", "category"]


# class FileUploadForm(forms.ModelForm):
#     class Meta:
#         model = StoredFile
#         fields = ["folder", "course", "file"]


# class FolderForm(forms.ModelForm):
#     class Meta:
#         model = Folder
#         fields = ["category", "name"]



# class SemesterForm(forms.ModelForm):
#     class Meta:
#         model = Semester
#         fields = ['name', 'start_date', 'end_date', 'is_active']
#         widgets = {
#             'start_date': forms.DateInput(attrs={'type': 'date'}),
#             'end_date': forms.DateInput(attrs={'type': 'date'}),
#         }




# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['semester', 'name', 'course_code', 'teacher_name', 'total_class_planned']




# class ClassSessionForm(forms.ModelForm):
#     class Meta:
#         model = ClassSession
#         fields = ['course', 'date', 'start_time']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#             'start_time': forms.TimeInput(attrs={'type': 'time'}),
#         }


# class CourseMarkForm(forms.ModelForm):
#     class Meta:
#         model = CourseMark
#         fields = ['mid1', 'mid2', 'presentation','assignment', 'final']