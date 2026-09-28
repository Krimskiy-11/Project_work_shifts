from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from tasks.views import TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("admin/", admin.site.urls),
    # Маршруты роутера для задач (/api/tasks/)
    path("api/", include(router.urls)),
    # Подключаем URLs из приложения users (/api/users/me/)
    path("api/", include("users.urls")),
    # Эндпоинт получения токена по логину/паролю
    path("api/api-token-auth/", obtain_auth_token),
    # Маршрут для /api/tasks/
    path('api/', include('tasks.urls')),
]
