# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .form import UserProfileForm, PinForm
from .models import UserProfile, Pin


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


# @login_required
# def edit_profile(request):
#     try:
#         user_profile = request.user.userprofile
#     except UserProfile.DoesNotExist:
#         user_profile = UserProfile.objects.create(user=request.user)
#         form = UserProfileForm(instance=user_profile)
#
#         if request.method == "POST":
#             form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#             print(12333)
#         if form.is_valid():
#             form.save()
#             print(56678)
#             return redirect("profile")
#     else:
#         form = UserProfileForm(instance=user_profile)
#
#     return render(request, "edit_profile.html", {"form": form})


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_profile = UserProfile.objects.get_or_create(user=request.user)

        user_form = UserProfileForm(request.POST, instance=request.user.userprofile)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect("edit_profile")

    else:
        user_profile = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserProfileForm(instance=request.user.userprofile)

        return render(request, "edit_profile.html", {"user_form": user_form})


@login_required(login_url="login")
def create_pin(request):
    if request.method == "POST":

        user_profile = UserProfile.objects.get_or_create(user=request.user)
        form = PinForm(request.POST, request.FILES)
        if form.is_valid():
            pin = form.save(commit=False)
            pin.user = request.user.userprofile
            pin.save()
            return redirect("pin_detail", pk=pin.pk)
    else:
        form = PinForm()
    return render(request, "add_pin.html", {"form": form})


@login_required(login_url="login")
def update_pin(request, pk):
    pin = get_object_or_404(Pin, pk=pk)
    if request.method == "POST":
        form = PinForm(request.POST, request.FILES, instance=pin)
        if form.is_valid():
            form.save()
            return redirect("pin_detail", pk=pin.pk)
    else:
        form = PinForm(instance=pin)
    return render(request, "update_pin.html", {"form": form})


@login_required(login_url="login")
def delete_pin(request, pk):
    pin = get_object_or_404(Pin, pk=pk)
    if request.method == "POST":
        pin.delete()
        return redirect("pin_list")
    return render(request, "delete_pin.html", {"pin": pin})


@login_required(login_url="login")
def pin_detail(request, pk):
    pin = get_object_or_404(Pin, pk=pk)
    return render(request, "pin_detail.html", {"pin": pin})


@login_required(login_url="login")
def pin_list(request):
    pins = Pin.objects.all()
    return render(request, "pin_list.html", {"pins": pins})
