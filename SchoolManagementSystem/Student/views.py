# Student Dashboard
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from SchoolAdmin.models import Announcement,Attendance
from Teacher.models import Assignment,Mark,Note
from django.contrib import messages
# Download notes
@login_required
def student_notes(request):
    student = request.user.student
    notes = Note.objects.filter(
        division=student.division
    )

    return render(request, "student_notes.html", {"notes": notes})

#Assignment Upload


from .models import StudentSubmission


@login_required
def student_assignments(request):

    # Get logged-in student
    student = request.user.student

    # Get assignments of student's division
    assignments = Assignment.objects.filter(
        division=student.division
    ).order_by("-created_at")

    if request.method == "POST":
        assignment_id = request.POST.get("assignment_id")
        file = request.FILES.get("file")

        assignment = get_object_or_404(Assignment, id=assignment_id)

        # Prevent duplicate submission
        if StudentSubmission.objects.filter(
            student=student,
            assignment=assignment
        ).exists():
            messages.error(request, "You have already submitted this assignment.")
            return redirect("student_assignments")

        # Save submission
        StudentSubmission.objects.create(
            student=student,
            assignment=assignment,
            file=file
        )

        messages.success(request, "Assignment submitted successfully!")
        return redirect("student_assignments")

    context = {
        "assignments": assignments
    }

    return render(request, "student_assignments.html", context)

# Attendance Graph

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from SchoolAdmin.models import Attendance
from collections import defaultdict
import json

@login_required
def attendance_graph(request):

    student = request.user.student

    # Get attendance records of this student
    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by("date")

    monthly_data = defaultdict(lambda: {"present": 0, "total": 0})

    for record in attendance_records:
        month = record.date.strftime("%b %Y")

        monthly_data[month]["total"] += 1

        if record.status:   # True means Present
            monthly_data[month]["present"] += 1

    months = []
    percentages = []

    for month, data in monthly_data.items():
        months.append(month)

        if data["total"] > 0:
            percentage = (data["present"] / data["total"]) * 100
        else:
            percentage = 0

        percentages.append(round(percentage, 2))

    context = {
        "months": json.dumps(months),
        "percentages": json.dumps(percentages)
    }

    return render(request, "attendance_graph.html", context)

# Students Mark



@login_required
def student_marks(request):

    student = request.user.student

    selected_exam = request.GET.get("exam")

    marks = []
    total_obtained = 0
    total_max = 0
    percentage = 0

    if selected_exam:
        marks = Mark.objects.filter(
            student=student,
            exam=selected_exam
        ).select_related("subject")

        for mark in marks:
            total_obtained += float(mark.marks_obtained)
            total_max += float(mark.max_marks)

        if total_max > 0:
            percentage = round((total_obtained / total_max) * 100, 2)

    context = {
        "marks": marks,
        "selected_exam": selected_exam,
        "exam_choices": Mark.EXAM_TYPES,
        "total_obtained": total_obtained,
        "total_max": total_max,
        "percentage": percentage,
    }

    return render(request, "student_marks.html", context)
