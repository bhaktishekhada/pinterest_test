# Create your views here.

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .form import UserProfileForm
from .models import UserProfile, Follow


def home(request):
    return render(request, "home.html")


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
                userprofile = UserProfile.objects.create(
                    user=user, profile_picture=None, bio=None
                )
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

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")


@login_required(login_url="login/")
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
            return redirect("home")  # Redirect to home after saving

    return render(
        request, "edit_profile.html", {"userprofile": userform, "user": userprofile}
    )


@login_required
def follow_user(request, user_id):
    # Get the user to follow
    user_to_follow = get_object_or_404(UserProfile, id=user_id)

    # Ensure the user is not trying to follow themselves
    if user_to_follow == request.user.userprofile:
        return HttpResponse("You cannot follow yourself.", status=400)

    # Create the follow relationship
    Follow.objects.get_or_create(
        follower=request.user.userprofile, following=user_to_follow
    )
    return redirect(
        "profile", user_id=user_to_follow.id
    )  # Redirect to the followed user's profile


@login_required
def unfollow_user(request, user_id):
    # Get the user to unfollow
    user_to_unfollow = get_object_or_404(UserProfile, id=user_id)

    # Remove the follow relationship
    Follow.objects.filter(
        follower=request.user.userprofile, following=user_to_unfollow
    ).delete()
    return redirect(
        "profile", user_id=user_to_unfollow.id
    )  # Redirect to the unfollowed user's profile


@login_required
def user_profile(request, user_id):
    # Get the user profile to display
    user_profile = get_object_or_404(UserProfile, id=user_id)

    # Get the list of followers and following
    followers = user_profile.followers.all()
    following = user_profile.following.all()

    context = {
        "user_profile": user_profile,
        "followers": followers,
        "following": following,
    }
    return render(request, "user_profile.html", context)


@login_required
def my_profile(request):
    # Get the logged-in user's profile
    user_profile = request.user.userprofile

    # Get the list of followers and following
    followers = user_profile.followers.all()
    following = user_profile.following.all()

    context = {
        "user_profile": user_profile,
        "followers": followers,
        "following": following,
    }
    return render(request, "login.html", context)


# def logout_view(request):
#     logout(request.user)
#     return redirect("home")
