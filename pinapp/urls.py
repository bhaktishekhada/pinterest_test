from django.urls import path

from pinapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("pins/create/", views.create_pin, name="create_pin"),
    path("pin/edit/<int:pk>/", views.edit_pin, name="edit_pin"),
    path("pins/<int:pk>/edit/", views.update_pin, name="update_pin"),
    path("pins/<int:pk>/delete/", views.delete_pin, name="delete_pin"),
    path("pins/", views.pin_list, name="pin_list"),
    path("pins/<int:pk>/", views.pin_detail, name="pin_detail"),
    path("create_board/", views.create_board, name="create_board"),
    path("logout/", views.logout_view, name="logout"),
]
