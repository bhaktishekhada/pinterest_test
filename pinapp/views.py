
# Create your views here.
from profile import Profile

from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from pinapp.form import UserProfileForm
from .models import UserProfile


def home(request):
    return render(request, 'home.html')


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
                userprofile = UserProfile.objects.create(user=user, profile_picture=None, bio=None)
                userprofile.save()
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

        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
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


# def edit_profile(request):
#
#     if request.method == "POST":
#         user_profile = get_object_or_404(Profile, user=request.user)
#         user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#         # print(request.FILES)
#         # print(user_form.profile_picture)
#         if user_form.is_valid():
#             user_form.save()
#             print(2345)
#
#             messages.success(request, "Your profile has been updated successfully!")
#             return redirect("edit_profile")
#     else:
#         userprofile = None
#         try:
#             userprofile = request.user.userprofile
#         except Exception as e:
#             print(e)
#         form = UserProfileForm(instance=userprofile)
#
#         user_form = UserProfileForm(instance=user_profile)
#         print(23465987)
#
#     context = {"user_form": user_form}
#
#     return render(request, "edit_profile.html", context)


# @login_required
# def edit_profile(request):
#     # Retrieve the profile instance for the logged-in user
#     user_profile, created = Profile.objects.get_or_create(user=request.user)

#     if request.method == "POST":
#         # Pass the profile instance to the form
#         user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#         if user_form.is_valid():
#             user_form.save()
#             return redirect(
#                 "user-profile"
#             )  # Redirect to a user profile page or any other view
#     else:
#         # Pre-fill the form with the user's profile data
#         user_form = UserProfileForm(instance=user_profile)

#     context = {"user_form": user_form}
#     return render(request, "edit_profile.html", context)


@login_required(login_url='login/')
def editprofile(request):
    user = request.user

    try:
        userprofile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        userprofile = None

    if userprofile is None:
        userprofile = UserProfile(user=user)
        userprofile.save()
    
    userform = UserProfileForm(instance=userprofile)

    if request.method == "POST":
        userform = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if userform.is_valid():
            userform.save()
            return redirect('home')  # Redirect to home after saving

    return render(request, 'edit_profile.html', {'userprofile': userform, 'user':userprofile})    

        
        
# def logout_view(request):
#     logout(request.user)
#     return redirect("home")

