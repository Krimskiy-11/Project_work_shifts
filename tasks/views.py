from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet для работы с задачами:
    - GET /api/tasks/ -> Список задач (разграничен по ролям)
    - POST /api/tasks/ -> Создание задачи (автоматически проставляет created_by)
    - GET /api/tasks/{id}/ -> Просмотр задачи
    - PATCH/PUT /api/tasks/{id}/ -> Обновление (статуса, исполнителя, названия)
    - DELETE /api/tasks/{id}/ -> Удаление задачи
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Если роли прописаны в модели User (например, EMPLOYEE)
        if getattr(user, 'role', '') == 'EMPLOYEE':
            # Сотрудник видит только назначенные ему задачи
            return Task.objects.filter(assigned_to=user)

        # Менеджеры и администраторы видят все задачи
        return Task.objects.all()

    def perform_create(self, serializer):
        # При создании задачи менеджер (текущий пользователь) автоматически становится created_by
        serializer.save(created_by=self.request.user)