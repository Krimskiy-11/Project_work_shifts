from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Колонки, отображаемые в таблице пользователей
    list_display = ("username", "email", "first_name", "last_name", "department", "role", "is_staff")

    # Фильтры в правой панели
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    # Поля, по которым работает поиск
    search_fields = ("username", "first_name", "last_name", "email", "department")

    # Добавление поля role в форму редактирования пользователя в админке
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("role", "department",)}),
    )

    # Добавление поля role в форму создания пользователя
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Дополнительная информация", {"fields": ("role", "department",)}),
    )