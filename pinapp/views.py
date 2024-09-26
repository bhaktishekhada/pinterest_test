# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .form import UserProfileForm
from .models import UserProfile


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email
                )
                user.save()
                messages.success(request, "You are now registered and can log in")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "register.html")


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("edit_profile")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")


@login_required
def edit_profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        form = UserProfileForm(instance=user_profile)

        if request.method == "POST":
            form = UserProfileForm(
                request.POST, request.FILES, instance=request.user.userprofile
            )
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, "edit_profile.html", {"form": form})
