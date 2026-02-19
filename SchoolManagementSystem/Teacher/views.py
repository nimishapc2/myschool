from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from SchoolAdmin.models import TeacherAssignment,Teacher,Student,Subject,Division
from Teacher.models import Mark,Assignment,Note
from django.contrib import messages


@login_required
def teacher_assignments(request):

    # Allow only TEACHER role
    if request.user.role != 'TEACHER':
        return render(request, 'unauthorized.html')

    # Get the teacher linked to logged-in user
    teacher = get_object_or_404(Teacher, user=request.user)

    # Fetch only assignments of this teacher
    assignments = TeacherAssignment.objects.filter(
        teacher=teacher
    ).select_related('subject', 'division')

    return render(request, 'teacher_assignments.html', {
        'assignments': assignments
    })

# Add Marks

@login_required
def add_marks(request):

    if request.user.role != 'TEACHER':
        return render(request, 'unauthorized.html')

    teacher = get_object_or_404(Teacher, user=request.user)

    assignments = TeacherAssignment.objects.filter(
        teacher=teacher
    ).select_related('subject', 'division')

    division_ids = assignments.values_list('division_id', flat=True)
    students = Student.objects.filter(division_id__in=division_ids)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        exam = request.POST.get('exam')
        marks_obtained = request.POST.get('marks_obtained')
        max_marks = request.POST.get('max_marks')

        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)

        Mark.objects.create(
            student=student,
            subject=subject,
            teacher=teacher,
            exam=exam,
            marks_obtained=marks_obtained,
            max_marks=max_marks
        )
        messages.success(request, "Announcement updated successfully")
        return redirect('add_marks')

    return render(request, 'add_marks.html', {
        'assignments': assignments,
        'students': students,
        'exam_choices': Mark.EXAM_TYPES
    })

#Inline edit and delete
@login_required
def view_marks(request):

    if request.user.role != 'TEACHER':
        return render(request, 'unauthorized.html')

    teacher = get_object_or_404(Teacher, user=request.user)

    assignments = TeacherAssignment.objects.filter(
        teacher=teacher
    ).select_related('subject', 'division')

    division_ids = assignments.values_list('division_id', flat=True)
    subject_ids = assignments.values_list('subject_id', flat=True)

    selected_division = request.GET.get('division')
    selected_subject = request.GET.get('subject')

    # BASE QUERY
    marks = Mark.objects.filter(
        teacher=teacher,
        student__division_id__in=division_ids,
        subject_id__in=subject_ids
    ).select_related('student', 'subject')

    # FILTERING
    if selected_division:
        marks = marks.filter(student__division_id=selected_division)

    if selected_subject:
        marks = marks.filter(subject_id=selected_subject)

    # 🔥 HANDLE UPDATE
    if request.method == "POST":
        action = request.POST.get("action")
        mark_id = request.POST.get("mark_id")

        mark = get_object_or_404(Mark, id=mark_id, teacher=teacher)

        if action == "update":
            mark.marks_obtained = request.POST.get("marks_obtained")
            mark.max_marks = request.POST.get("max_marks")
            mark.save()

        elif action == "delete":
            mark.delete()

        return redirect(request.path)

    context = {
        'marks': marks,
        'divisions': Division.objects.filter(id__in=division_ids),
        'subjects': Subject.objects.filter(id__in=subject_ids),
        'selected_division': selected_division,
        'selected_subject': selected_subject
    }

    return render(request, 'view_marks.html', context)

# Post Assignment
@login_required
def post_assignment(request):

    if request.user.role != 'TEACHER':
        return render(request, 'unauthorized.html')

    teacher = get_object_or_404(Teacher, user=request.user)

    assignments = TeacherAssignment.objects.filter(
        teacher=teacher
    ).select_related('subject', 'division', 'division__school_class')

    if request.method == 'POST':

        division_id = request.POST.get('division')
        subject_id = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        division = get_object_or_404(Division, id=division_id)
        subject = get_object_or_404(Subject, id=subject_id)

        Assignment.objects.create(
            teacher=teacher,
            school_class=division.school_class,
            division=division,
            subject=subject,
            title=title,
            description=description,
            due_date=due_date
        )

        messages.success(request, "Post assignment successfully")
        return redirect(request.path)
    return render(request, 'post_assignment.html', {
        'assignments': assignments
    })


# Manage Assignments
@login_required
def manage_assignments(request):

    if request.user.role != 'TEACHER':
        return render(request, 'unauthorized.html')

    teacher = get_object_or_404(Teacher, user=request.user)

    assignments = Assignment.objects.filter(
        teacher=teacher
    ).select_related('division', 'subject', 'school_class').order_by('-created_at')

    # HANDLE INLINE UPDATE / DELETE
    if request.method == "POST":

        action = request.POST.get("action")
        assignment_id = request.POST.get("assignment_id")

        assignment = get_object_or_404(
            Assignment,
            id=assignment_id,
            teacher=teacher
        )

        if action == "update":
            assignment.title = request.POST.get("title")
            assignment.description = request.POST.get("description")
            assignment.due_date = request.POST.get("due_date")
            assignment.save()

        elif action == "delete":
            assignment.delete()

        return redirect('manage_assignments')

    return render(request, 'manage_assignments.html', {
        'assignments': assignments
    })
 
 # Upload Notes
@login_required
def upload_notes(request):

    if request.user.role != 'TEACHER':
        return render(request, 'unauthorized.html')

    teacher = get_object_or_404(Teacher, user=request.user)

    assignments = TeacherAssignment.objects.filter(
        teacher=teacher
    ).select_related('division', 'subject', 'division__school_class')

    if request.method == 'POST':

        division_id = request.POST.get('division')
        subject_id = request.POST.get('subject')
        lesson_number = request.POST.get('lesson_number')
        title = request.POST.get('title')
        file = request.FILES.get('file')

        division = get_object_or_404(Division, id=division_id)
        subject = get_object_or_404(Subject, id=subject_id)

        Note.objects.create(
            teacher=teacher,
            school_class=division.school_class,
            division=division,
            subject=subject,
            lesson_number=lesson_number,
            title=title,
            file=file
        )
        messages.success(request, "Notes uploaded successfully!")
        return redirect(request.path)


    return render(request, 'upload_notes.html', {
        'assignments': assignments
    })

# View notes,edit and delete
from django.contrib import messages

@login_required
def manage_notes(request):

    if request.user.role != 'TEACHER':
        return render(request, 'unauthorized.html')

    teacher = get_object_or_404(Teacher, user=request.user)

    notes = Note.objects.filter(
        teacher=teacher
    ).select_related('division', 'subject', 'school_class').order_by('-uploaded_at')

    if request.method == "POST":

        action = request.POST.get("action")
        note_id = request.POST.get("note_id")

        note = get_object_or_404(Note, id=note_id, teacher=teacher)

        if action == "update":
            note.lesson_number = request.POST.get("lesson_number")
            note.title = request.POST.get("title")

            # If new file uploaded
            if request.FILES.get("file"):
                note.file = request.FILES.get("file")

            note.save()
            messages.success(request, "Note updated successfully!")

        elif action == "delete":
            note.delete()
            messages.success(request, "Note deleted successfully!")

        return redirect(request.path)

    return render(request, 'manage_notes.html', {
        'notes': notes
    })

# Student Dashboard

from django.db.models import Avg, Sum
from .models import Student
from Teacher.models import Note, Assignment, Mark
from SchoolAdmin.models import Announcement,Attendance
@login_required
def student_dashboard(request):

    if request.user.role != "STUDENT":
        return render(request, "unauthorized.html")

    student = get_object_or_404(Student, user=request.user)

    # 1️⃣ Announcements
    announcements = Announcement.objects.all().order_by('-created_at')

    # 2️⃣ Assignments for student class
    assignments = Assignment.objects.filter(
        school_class=student.school_class,
        division=student.division
    ).order_by('-created_at')

    # 3️⃣ Notes for download
    notes = Note.objects.filter(
        school_class=student.school_class,
        division=student.division
    )

    # 4️⃣ Attendance Percentage
    total_classes = Attendance.objects.filter(student=student).count()
    present_count = Attendance.objects.filter(
        student=student,
        status="Present"
    ).count()

    attendance_percentage = 0
    if total_classes > 0:
        attendance_percentage = round((present_count / total_classes) * 100, 2)

    # 5️⃣ Progress Card
    marks = Mark.objects.filter(student=student)

    overall_average = marks.aggregate(avg=Avg('mark'))['avg']
    if overall_average:
        overall_average = round(overall_average, 2)
    else:
        overall_average = 0

    return render(request, "student_dashboard.html", {
        "student": student,
        "announcements": announcements,
        "assignments": assignments,
        "attendance_percentage": attendance_percentage,
        "overall_average": overall_average,
        "notes": notes,
    })
