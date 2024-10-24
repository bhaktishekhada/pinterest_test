# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .form import UserProfileForm, PinForm, BoardForm
from .models import UserProfile, Pin


def home(request):
    pins = Pin.objects.all()
    # paginator = Paginator(pins, 3)
    page = request.GET.get("page", 1)
    if page == "1":
        page_post = 5
    else:
        page_post = 3
    paginator = Paginator(pins, page_post)

    print("page", page)
    try:
        pins = paginator.page(page)
    except PageNotAnInteger:
        pins = paginator.page(1)
    except EmptyPage:
        pins = paginator.page(paginator.num_pages)
    return render(request, "pin_list.html", {"pins": pins})


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

                login(request, user)
                messages.success(request, "You are now registered and can log in")
                return redirect("home")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "register.html")


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]

        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # if request.user.is_authenticated:
            # logout(request)
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")


@login_required(login_url="login")
def profile_view(request):
    # Get the logged-in user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)

    return render(request, "user_profile.html", {"user_profile": user_profile})


@login_required(login_url="login")
def edit_profile(request):
    if request.method == "POST":
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        print(" hhhnjhhhhhhh", request.FILES)
        if user_form.is_valid():
            user_form.save()
            print(" hhhnjhhhhhhh", request.FILES)
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("home")
    else:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserProfileForm(instance=user_profile)

    return render(request, "edit_profile.html", {"form": user_form})


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
    print(pin.user)
    userprofile = UserProfile.objects.get(user=request.user)
    print(userprofile)
    if pin.user == userprofile:
        if request.method == "POST":
            form = PinForm(request.POST, request.FILES, instance=pin)
            if form.is_valid():
                form.save()
                return redirect("pin_detail", pk=pin.pk)
        else:
            form = PinForm(instance=pin)
    else:
        print(f"Object Owner: {pin.user}, Logged-in User: {request.user}")
        raise PermissionDenied("You don't own this object")
    return render(request, "edit_pin.html", {"form": form})


@login_required(login_url="login")
def delete_pin(request, pk):
    pin = get_object_or_404(Pin, pk=pk)

    # Ensure that the logged-in user owns the pin (check via UserProfile)
    user_profile = UserProfile.objects.get(user=request.user)
    if pin.user != user_profile:
        # Prevent unauthorized access by raising a 403 Forbidden error
        messages.error(request, "You do not have permission to delete this pin.")
        return redirect("home")

    if request.method == "POST":
        pin.delete()
        return redirect("home")

    return render(request, "delete_pin.html", {"pin": pin})


@login_required(login_url="login")
def edit_pin(request, pk):
    # Get the pin object by primary key (pk)
    pin = get_object_or_404(Pin, pk=pk)

    # Ensure that the logged-in user owns the pin (check via UserProfile)
    user_profile = UserProfile.objects.get(user=request.user)
    if pin.user != user_profile:
        # Prevent unauthorized access by raising a 403 Forbidden error
        messages.error(request, "You do not have permission to edit this pin.")
        return redirect("home")
        # raise PermissionDenied("You do not have permission to edit this pin.")

    # Handle form submission for editing the pin
    if request.method == "POST":
        form = PinForm(request.POST, request.FILES, instance=pin)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PinForm(instance=pin)

    # Render the edit pin page with the form
    return render(request, "edit_pin.html", {"form": form})


def pin_detail(request, pk):
    pin = get_object_or_404(Pin, pk=pk)
    return render(request, "pin_detail.html", {"pin": pin})


# def pin_list(request):
#     pins = Pin.objects.all()
#
#     return render(request, "pin_list.html", {"pins": pins})


# def pin_list(request):
#     pin_list = Pin.objects.all()
#     paginator = Paginator(pin_list, 10)  # Show 10 pins per page
#     print(paginator.pin, 10)
#     page_number = request.GET.get("page", 1)
#     print(f"Current page number: {page_number}")
#
#     try:
#         page_number = int(page_number)
#     except ValueError:
#         page_number = 1
#     pins = paginator.get_page(page_number)
#
#     return render(request, "pin_list.html", {"pins": pins})


@login_required(login_url="login")
def create_board(request):
    if request.method == "POST":

        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user_profile = request.user.userprofile
            board.save()
            return redirect("dashboard", username=request.user.username)
    else:
        form = BoardForm()
    return render(request, "create_board.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect("login")
