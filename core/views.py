from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from urllib3 import request
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

from .forms import (
    SemesterForm, 
    CourseForm,
    ClassSessionForm, 
    CourseMarkForm, 
    FileUploadForm, 
    FolderForm,
    AssessmentForm,
    CalendarEventForm,
    SignupForm
    )

from datetime import date, timedelta
from django.db.models import Q, Count

from .utils import attendance_summary, missable_classes, get_general_category

from django.utils import timezone

from django.http import JsonResponse
from django.views.decorators.http import require_POST


class UserLoginView(LoginView):
    template_name = 'auth/login.html'



class UserLoginView(LoginView):
    template_name = 'auth/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_approved:
            return render(
                self.request,
                'auth/pending.html'
            )
        return super().form_valid(form)



@login_required
def approve_user(request, user_id):
    if request.user.is_superuser:
        user = User.objects.get(id=user_id)
        user.is_approved = True
        user.save()
    return redirect('approve_users')


@login_required
def dashboard(request):
    courses = Course.objects.filter(user=request.user)

    total_attended = 0
    total_effective = 0
    course_data = []

    for course in courses:
        summary = attendance_summary(course)

        total_attended += summary['attended']
        total_effective += summary['total_effective']

        course_data.append({
            'course': course,
            'percentage': summary['percentage'],
            'attended': summary['attended'],
            'total': summary['total_effective'],
            'warning': summary['percentage'] < 75
        })

    overall_percentage = (
        (total_attended / total_effective) * 100
        if total_effective > 0 else 0
    )

    # Active semester summary
    active_semester = Semester.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    semester_courses = (
        active_semester.courses.count()
        if active_semester else 0
    )

    return render(request, 'dashboard.html', {
        'overall_percentage': round(overall_percentage, 2),
        'course_data': course_data,
        'active_semester': active_semester,
        'semester_courses': semester_courses
    })
    return render(request, 'dashboard.html')


def signup(request):
    form = SignupForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = True
        user.is_approved = False
        user.save()
        return render(request, 'auth/pending.html')

    return render(request, 'auth/signup.html', {'form': form})



@login_required
def approve_users(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    users = User.objects.filter(is_approved=False)

    return render(request, 'admin/approve_users.html', {
        'users': users
    })



@login_required
def semester_list(request):
    semesters = Semester.objects.filter(user=request.user)
    context ={
        'semesters':semesters
    }
    return render(request, 'semester/list.html', context)

@login_required
def semester_create(request):
    form = SemesterForm(request.POST or None)
    if form.is_valid():
        semester = form.save(commit =False)
        semester.user = request.user
        semester.save()
        return redirect('semester_list')
    return render(request, 'semester/form.html', {'form': form})

@login_required
def semester_delete(request, pk):
    semester = get_object_or_404(Semester, pk=pk, user=request.user)
    semester.delete()
    return redirect('semester_list')


@login_required
def course_list(request):
    courses = Course.objects.filter(user=request.user)
    return render(request, 'course/list.html', {'courses': courses})

@login_required
def course_create(request):
    form =CourseForm(request.POST or None)
    form.fields['semester'].queryset = Semester.objects.filter(user=request.user)
    if form.is_valid():
        course = form.save(commit=False)
        course.user = request.user
        course.save()
        return redirect('course_list')
    return render(request, 'course/form.html', {'form': form})


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    course.delete()
    return redirect('course_list')


@login_required
def plan_class(request):
    form = ClassSessionForm(request.POST or None)
    form.fields['course'].queryset = Course.objects.filter(user=request.user)

    if form.is_valid():
        session = form.save(commit=False)
        session.user = request.user
        session.save()
        return redirect('tomorrow_classes')

    return render(request, 'class_session/form.html', {'form': form})


@login_required
def tomorrow_classes(request):
    tomorrow = date.today() + timedelta(days=1)
    sessions = ClassSession.objects.filter(
        user=request.user,
        date=tomorrow
    )

    return render(request, 'class_session/tomorrow.html', {
        'sessions': sessions,
        'tomorrow': tomorrow
    })

@login_required
def edit_class_session(request, pk):
    session = get_object_or_404(ClassSession, pk=pk, user=request.user)

    if session.status != 'planned':
        return redirect('tomorrow_classes')

    form = ClassSessionForm(request.POST or None, instance=session)
    form.fields['course'].queryset = Course.objects.filter(user=request.user)

    if form.is_valid():
        form.save()
        return redirect('tomorrow_classes')

    return render(request, 'class_session/form.html', {'form': form})

@login_required
def mark_attendance(request):
    today = date.today()

    sessions = ClassSession.objects.filter(
        user = request.user,
        date__lte = today,
        status = 'planned'
    ).order_by('-date', '-start_time')

    context ={
        'sessions': sessions,
    }
    return render(request, 'attendance/mark.html',context)


# @login_required
# def update_attendance_status(request, pk,status):
#     session = get_object_or_404(
#         ClassSession,
#         pk=pk,
#         user=request.user
#     )

#     if status in ['completed', 'cancelled', 'no_attendance']:
#         return redirect('mark_attendance')
    
#     session.status = status
#     session.save()

#     return redirect('mark_attendance')

@login_required
def update_attendance_status(request, pk):
    if request.method != 'POST':
        return redirect('mark_attendance')

    status = request.POST.get('status')

    # if status not in ['completed', 'cancelled', 'no_attendance']:
    #     return redirect('mark_attendance')

    if status not in ['completed', 'absent', 'cancelled', 'no_attendance']:
        return redirect('mark_attendance')

    session = get_object_or_404(
        ClassSession,
        pk=pk,
        user=request.user,
        status='planned'
    )

    session.status = status
    session.save()

    return redirect('mark_attendance')



@login_required
def course_attendance_stats(request):
    courses = Course.objects.filter(user=request.user)

    stats = []
    for course in courses:
        total_classes = ClassSession.objects.filter(
            course=course,
            status='completed'
        ).count()

        total_possible = ClassSession.objects.filter(
            course=course
        ).exclude(status__in=['cancelled', 'no_attendance']).count()

        percentage = (
            (total_classes / total_possible) * 100
            if total_possible > 0 else 0
        )

        stats.append({
            'course': course,
            'attended': total_classes,
            'total': total_possible,
            'percentage': round(percentage, 2)
        })

    return render(request, 'attendance/stats.html', {'stats': stats})


@login_required
def smart_attendance(request):
    courses = Course.objects.filter(user=request.user)

    data = []
    for course in courses:
        summary = attendance_summary(course)
        missable = missable_classes(course)

        data.append({
            'course': course,
            'summary': summary,
            'missable': missable,
            'warning': summary['percentage'] < 75
        })

    return render(request, 'attendance/smart.html', {'data': data})


@login_required
def marks_overview(request):
    courses = Course.objects.filter(user=request.user)
    
    data = []

    for course in courses:
        mark, _ = CourseMark.objects.get_or_create(
            user=request.user,
            course=course
        )

        data.append({
            'course': course,
            'mark': mark
        })

    return render(request, 'marks/overview.html', {'data': data})


@login_required
def edit_marks(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        user=request.user
    )

    mark, _ = CourseMark.objects.get_or_create(
        user=request.user,
        course=course
    )

    form = CourseMarkForm(request.POST or None, instance=mark)

    if form.is_valid():
        form.save()
        return redirect('marks_overview')

    return render(request, 'marks/form.html', {
        'form': form,
        'course': course
    })


# @login_required
# def file_hub(request):
#     categories = FileCategory.objects.filter(user=request.user)
#     folders = Folder.objects.filter(user=request.user)
#     files = StoredFile.objects.filter(user=request.user).order_by("-uploaded_at")

#     upload_form = FileUploadForm(request.POST or None, request.FILES or None)
#     upload_form.fields["folder"].queryset = folders
#     upload_form.fields["course"].queryset = Course.objects.filter(user=request.user)

#     if upload_form.is_valid():
#         obj = upload_form.save(commit=False)
#         obj.user = request.user
#         obj.original_name = obj.file.name
#         obj.size = obj.file.size
#         obj.save()
#         return redirect("file_hub")

#     return render(request, "files/hub.html", {
#         "categories": categories,
#         "folders": folders,
#         "files": files,
#         "upload_form": upload_form,
#     })

@login_required
def file_hub(request):
    categories = FileCategory.objects.filter(user=request.user)
    folders = Folder.objects.filter(user=request.user)

    category_id = request.GET.get("category")
    folders = Folder.objects.filter(user=request.user)
    if category_id:
        folders = folders.filter(category_id=category_id)

    return render(request, "files/hub.html", {
        "categories": categories,
        "folders": folders,
    })



@login_required
def folder_view(request, folder_id):
    folder = get_object_or_404(
        Folder,
        id=folder_id,
        user=request.user
    )

    files = StoredFile.objects.filter(
        user=request.user,
        folder=folder
    ).order_by("-uploaded_at")

    upload_form = FileUploadForm(request.POST or None, request.FILES or None)
    upload_form.fields["folder"].queryset = Folder.objects.filter(user=request.user)
    upload_form.fields["folder"].initial = folder

    if upload_form.is_valid():
        obj = upload_form.save(commit=False)
        obj.user = request.user
        obj.original_name = obj.file.name
        obj.size = obj.file.size
        obj.display_name = (
            upload_form.cleaned_data.get("display_name")
            or obj.original_name
        )
        obj.folder = folder
        obj.save()
        return redirect("folder_view", folder_id=folder.id)

    return render(request, "files/folder.html", {
        "folder": folder,
        "files": files,
        "upload_form": upload_form,
    })



# @login_required
# def create_folder(request):
#     form = FolderForm(request.POST or None)
#     form.fields["category"].queryset = FileCategory.objects.filter(user=request.user)

#     if form.is_valid():
#         folder = form.save(commit=False)
#         folder.user = request.user
#         folder.save()
#         return redirect("file_hub")

#     return render(request, "files/create_folder.html", {"form": form})



@login_required
def create_folder(request):
    form = FolderForm(request.POST or None)

    if form.is_valid():
        folder = form.save(commit=False)
        folder.user = request.user

        if not folder.category:
            folder.category = get_general_category(request.user)

        folder.save()
        return redirect("file_hub")

    return render(request, "files/create_folder.html", {"form": form})



@login_required
def edit_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    form = FolderForm(request.POST or None, instance=folder)
    if form.is_valid():
        form.save()
        return redirect("file_hub")

    return render(request, "files/edit_folder.html", {
        "form": form,
        "folder": folder
    })


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(StoredFile, id=file_id, user=request.user)
    file.file.delete(save=False)  # deletes from R2
    file.delete()
    return redirect(request.META.get("HTTP_REFERER", "file_hub"))


@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    for f in folder.files.all():
        f.file.delete(save=False)
        f.delete()

    folder.delete()
    return redirect("file_hub")


@login_required
@require_POST
def create_category_ajax(request):
    name = request.POST.get("name", "").strip()

    if not name:
        return JsonResponse({"error": "Category name required"}, status=400)

    category, created = FileCategory.objects.get_or_create(
        user=request.user,
        name=name
    )

    return JsonResponse({
        "id": category.id,
        "name": category.name
    })


@login_required
def semester_edit(request, pk):
    semester = get_object_or_404(
        Semester, pk=pk, user=request.user
    )
    form = SemesterForm(request.POST or None, instance=semester)

    if form.is_valid():
        form.save()
        return redirect('semester_list')

    return render(request, 'semester/form.html', {'form': form})


@login_required
def course_edit(request, pk):
    course = get_object_or_404(
        Course, pk=pk, user=request.user
    )
    form = CourseForm(request.POST or None, instance=course)
    form.fields['semester'].queryset = Semester.objects.filter(
        user=request.user
    )

    if form.is_valid():
        form.save()
        return redirect('course_list')

    return render(request, 'course/form.html', {'form': form})


@login_required
def assessment_edit(request, pk):
    assessment = get_object_or_404(
        Assessment, pk=pk, user=request.user
    )
    form = AssessmentForm(request.POST or None, instance=assessment)
    form.fields['course'].queryset = Course.objects.filter(
        user=request.user
    )

    if form.is_valid():
        form.save()
        return redirect('assessment_list')

    return render(request, 'assessment/form.html', {'form': form})


@login_required
def assessment_delete(request, pk):
    assessment = get_object_or_404(
        Assessment, pk=pk, user=request.user
    )
    assessment.delete()
    return redirect('assessment_list')


@login_required
def class_history_courses(request):
    courses = Course.objects.filter(user=request.user)
    return render(request, 'history/course_list.html', {
        'courses': courses
    })


@login_required
def class_history_detail(request, course_id):
    course = get_object_or_404(
        Course, id=course_id, user=request.user
    )

    sessions = ClassSession.objects.filter(
        course=course
    ).order_by('-date', '-start_time')

    return render(request, 'history/course_detail.html', {
        'course': course,
        'sessions': sessions
    })


@login_required
def assessment_create(request):
    form = AssessmentForm(request.POST or None)
    form.fields['course'].queryset = Course.objects.filter(user=request.user)

    if form.is_valid():
        assessment = form.save(commit=False)
        assessment.user = request.user
        assessment.save()
        return redirect('assessment_list')

    return render(request, 'assessment/form.html', {'form': form})


@login_required
def assessment_list(request):
    today = date.today()
    warning_date = today + timedelta(days=5)

    assessments = Assessment.objects.filter(
        user=request.user
    ).order_by('date')

    data = []
    for a in assessments:
        data.append({
            'assessment': a,
            'warning': today <= a.date <= warning_date
        })

    return render(request, 'assessment/list.html', {'data': data})



@login_required
def academic_calendar(request):
    events = []

    # 🟢 Classes
    for c in ClassSession.objects.filter(user=request.user):
        events.append({
            'title': c.course.name,
            'start': f"{c.date}T{c.start_time}",
            'color': '#22c55e',
            'extendedProps': {'type': 'class'}
        })

    # 🔴 Exams
    for a in Assessment.objects.filter(user=request.user):
        events.append({
            'title': f"{a.course.name} — {a.get_type_display()}",
            'start': a.date.isoformat(),
            'color': '#fca5a5',
            'extendedProps': {'type': 'exam'}
        })

    # 🟡 Global + User Events
    # custom_events = CalendarEvent.objects.filter(
    #     Q(is_global=True) |
    #     Q(user=request.user)
    # )

    custom_events = CalendarEvent.objects.filter(
        Q(is_global=True) |
        Q(user=request.user)
    )

    for e in custom_events:
        event = {
            'title': e.title,
            'start': e.start_date.isoformat(),
            'color': '#800080',
            'extendedProps': {'type': e.event_type}
        }

        if e.end_date:
            event['end'] = (e.end_date + timedelta(days=1)).isoformat()

        events.append(event)

    return render(request, 'calendar/main.html', {'events': events})



# @login_required
# def add_calendar_event(request):
#     form = CalendarEventForm(request.POST or None)

#     if form.is_valid():
#         event = form.save(commit=False)
#         event.user = request.user
#         event.save()
#         return redirect('academic_calendar')

#     return render(request, 'calendar/form.html', {'form': form})

@login_required
def add_calendar_event(request):
    form = CalendarEventForm(request.POST or None)

    if form.is_valid():
        event = form.save(commit=False)

        if request.user.is_superuser:
            # admin can create global events
            event.is_global = True
            event.user = None
        else:
            # normal user → personal event
            event.user = request.user
            event.is_global = False

        event.save()
        return redirect('academic_calendar')

    return render(request, 'calendar/form.html', {'form': form})
