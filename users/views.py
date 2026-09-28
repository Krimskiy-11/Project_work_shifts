from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User, Department


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    user = request.user
    return Response(
        {
            "id": user.id,
            "username": user.username,
            "role": getattr(user, "role", "EMPLOYEE"),
            "is_superuser": user.is_superuser,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    """
    Возвращает список всех пользователей с данными об их отделе.
    """
    # select_related оптиматизирует запрос к БД для получения связанных отделов
    users = User.objects.select_related("department").all().order_by("username")

    data = [
        {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": getattr(user, "role", "EMPLOYEE"),
            "department": user.department.id if user.department else None,
            "department_detail": {
                "id": user.department.id,
                "name": user.department.name,
            } if user.department else None,
        }
        for user in users
    ]
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def department_list_view(request):
    """
    Возвращает список всех отделов.
    """
    departments = Department.objects.all().order_by("name")
    data = [
        {
            "id": dept.id,
            "name": dept.name,
            "description": dept.description,
        }
        for dept in departments
    ]
    return Response(data)