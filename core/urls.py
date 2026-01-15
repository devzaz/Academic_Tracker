from django.urls import path
from . import views

urlpatterns = [
    # Semester URL list
    path('semesters/', views.semester_list, name='semester_list'),
    path('semesters/add/', views.semester_create, name='semester_create'),
    path('semesters/<int:pk>/delete/', views.semester_delete, name='semester_delete'),
    # Course URLs list
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Class Url list
    path('classes/plan/', views.plan_class, name='plan_class'),
    path('classes/tomorrow/', views.tomorrow_classes, name='tomorrow_classes'),
    path('classes/<int:pk>/edit/', views.edit_class_session, name='edit_class_session'),

    path(
        'attendance/', 
        views.mark_attendance, 
        name='mark_attendance'),

    path(
    'attendance/<int:pk>/update/',
    views.update_attendance_status,
    name='update_attendance_status'
    ),

    path(
        'attendance/stats/',
        views.course_attendance_stats,
        name='attendance_stats'
    ),

    path(
        'attendance/smart/', 
        views.smart_attendance, 
        name='smart_attendance'
    ),

    path('marks/', views.marks_overview, name='marks_overview'),
    path('marks/<int:course_id>/edit/', views.edit_marks, name='edit_marks'),

    path("files/", views.file_hub, name="file_hub"),
    path("files/folder/<int:folder_id>/", views.folder_view, name="folder_view"),
    path("files/folder/create/", views.create_folder, name="create_folder"),

    path("files/folder/<int:folder_id>/edit/", views.edit_folder, name="edit_folder"),

    path("files/file/<int:file_id>/delete/", views.delete_file, name="delete_file"),
    path("files/folder/<int:folder_id>/delete/", views.delete_folder, name="delete_folder"),

    path("files/category/create/", views.create_category_ajax, name="create_category_ajax"),

    path('semesters/<int:pk>/edit/', views.semester_edit, name='semester_edit'),

    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),

]
