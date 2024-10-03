from django.urls import path

from pinapp import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    # path("create_board/", views.create_board, name="create_board"),
    # path("add_pin/<int:board_id>/", views.add_pin, name="add_pin"),
    path("pins/create/", views.create_pin, name="create_pin"),
    path("pins/<int:pk>/edit/", views.update_pin, name="update_pin"),
    path("pins/<int:pk>/delete/", views.delete_pin, name="delete_pin"),
    path("pins/", views.pin_list, name="pin_list"),
    path("pins/<int:pk>/", views.pin_detail, name="pin_detail"),
]
