from django.urls import path

from .views import current_user_view, user_list_view, department_list_view

urlpatterns = [
    path("users/me/", current_user_view, name="current_user"),
    path("users/", user_list_view, name="user_list"),
    path("departments/", department_list_view, name="department_list"),
]
