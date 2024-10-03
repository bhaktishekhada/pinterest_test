from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    # path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("edit_profile/", views.editprofile, name="edit_profile"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    # path('logout/' , views.logout_view, name="logout"),
]
