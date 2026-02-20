from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from SchoolAdmin.models import Teacher,Student

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USERNAME:", username)
        print("PASSWORD:", password)

        user = authenticate(request, username=username, password=password)

        print("USER:", user)   # 👈 ADD THIS

        if user is not None:
            login(request, user)   # creates session
            print("LOGIN SUCCESS")

            if user.role == "ADMIN":
                return redirect("admin_dashboard")
            elif user.role == "TEACHER":
                return redirect("teacher_dashboard")
            elif user.role == "STUDENT":
                return redirect("student_dashboard")

        else:
            print("AUTH FAILED")

    return render(request, "login.html")


@login_required
def admin_dashboard(request):
    if request.user.role != "ADMIN":
        return redirect("login")

    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()

    context = {
        "total_teachers": total_teachers,
        "total_students": total_students,
    }

    return render(request, "admin_dashboard.html", context)



@login_required
def teacher_dashboard(request):
    return render(request, "teacher_dashboard.html")


@login_required
def student_dashboard(request):
    return render(request, "student_dashboard.html")


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to your login url name