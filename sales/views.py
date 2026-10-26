import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import DatabaseError, IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from employees.forms import EmployeeForm
from employees.models import Employee

logger = logging.getLogger(__name__)


def login_fun(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("txtname", "").strip()
        password = request.POST.get("txtpswd", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Incorrect username or password.")

    return render(request, "login.html")


def signup_fun(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("txtname1", "").strip()
        email = request.POST.get("txtmail1", "").strip().lower()
        password = request.POST.get("txtpswd1", "")
        password_confirmation = request.POST.get("txtpswd2", "")

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
        elif password != password_confirmation:
            messages.error(request, "The passwords do not match.")
        elif User.objects.filter(Q(username__iexact=username) | Q(email__iexact=email)).exists():
            messages.error(request, "Username or email already exists.")
        else:
            try:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
            except IntegrityError:
                messages.error(request, "Username or email already exists.")
            else:
                messages.success(request, "Your account was created. Please log in.")
                return redirect("log")

    return render(request, "signup.html")


@login_required(login_url="log")
@require_POST
def logout_fun(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("log")


@login_required(login_url="log")
def home(request):
    return render(
        request,
        "home.html",
        {"sales": not request.user.is_superuser, "users": request.user},
    )


@login_required(login_url="log")
def add_emp(request):
    form = EmployeeForm(
        request.POST if request.method == "POST" else None,
    )
    if request.method == "POST":
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
            except IntegrityError:
                logger.exception("Unable to create employee record")
                form.add_error("email", "An employee with this email already exists.")
            else:
                messages.success(request, "Employee added successfully.")
                return redirect("display")

    return render(request, "add.html", {"form": form})


@login_required(login_url="log")
def display_emp(request):
    try:
        employees = Employee.objects.all()
        # Evaluate inside the handler so database failures can be reported.
        employees = list(employees)
    except DatabaseError:
        logger.exception("Unable to load employee records")
        messages.error(request, "Employee records could not be loaded. Please try again.")
        employees = []

    return render(
        request,
        "display.html",
        {
            "employees": employees,
            "can_manage": True,
        },
    )


@login_required(login_url="log")
def update_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    form = EmployeeForm(
        request.POST if request.method == "POST" else None,
        instance=employee,
    )
    if request.method == "POST":
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
            except IntegrityError:
                logger.exception("Unable to update employee record %s", id)
                form.add_error("email", "An employee with this email already exists.")
            else:
                messages.success(request, "Employee updated successfully.")
                return redirect("display")

    return render(request, "add.html", {"form": form, "employee": employee})


@login_required(login_url="log")
@require_POST
def delete_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    try:
        with transaction.atomic():
            employee.delete()
    except DatabaseError:
        logger.exception("Unable to delete employee record %s", id)
        messages.error(request, "Employee could not be deleted. Please try again.")
    else:
        messages.success(request, "Employee deleted successfully.")
    return redirect("display")
