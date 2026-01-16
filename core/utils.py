from .models import ClassSession

from .models import FileCategory

def attendance_summary(course):
    session = ClassSession.objects.filter(course=course)

    attended = session.filter(status='completed').count()
    absent = session.filter(status='absent').count()
    ignored = session.filter(status__in=['cancelled', 'no_attendance']).count()
    planned = session.filter(status='planned').count()

    total_effective = attended + planned + absent

    percentage =(
        (attended / total_effective) * 100
        if total_effective > 0 else 0
    )

    return {
        'attended': attended,
        'planned': planned,
        'ignored': ignored,
        'absent': absent,
        'percentage': round(percentage, 2),
        'total_effective': total_effective
    }


def missable_classes(course, threshold=75):
    summary = attendance_summary(course)
    attended = summary['attended']
    planned = summary['planned']

    missable = 0

    for miss in range(planned+1):
        possible_total = attended + (planned - miss)
        if possible_total == 0:
            continue
    
        
        percentage = (attended/possible_total)*100

        if percentage >= threshold:
            missable =  miss
        else:
            break

    return missable

def get_general_category(user):
    category, _ = FileCategory.objects.get_or_create(
        user=user,
        name="General"
    )
    return category


#file sharing system

import zipfile
from io import BytesIO
from django.core.files.base import ContentFile

def create_folder_zip(folder):
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in folder.files.all():
            # 🔥 STORAGE-SAFE FILE READ
            f.file.open("rb")
            try:
                zipf.writestr(
                    f.display_name or f.original_name,
                    f.file.read()
                )
            finally:
                f.file.close()

    buffer.seek(0)
    return ContentFile(buffer.read())