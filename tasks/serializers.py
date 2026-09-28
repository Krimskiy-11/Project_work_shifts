from rest_framework import serializers
from users.models import User
from .models import Task


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "role", "department"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserShortSerializer(source="assigned_to", read_only=True)
    created_by_detail = UserShortSerializer(source="created_by", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "created_at",
            "assigned_to",
            "assigned_to_detail",
            "created_by",
            "created_by_detail",
        ]
        read_only_fields = ["created_by", "created_at"]