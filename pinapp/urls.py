from django.urls import path

from pinapp import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]
