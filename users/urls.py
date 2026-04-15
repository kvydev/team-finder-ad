from django.urls import path

from users.views import (
    user_list,
    user_detail,
    register,
    login,
    edit_profile,
    change_password,
    logout,
)

app_name = "users"
urlpatterns = [
    path("list/", user_list, name="users_list"),
    path("<int:user_id>/", user_detail, name="user_detail"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("change-password/", change_password, name="change_password"),
    path("logout/", logout, name="logout"),
]
