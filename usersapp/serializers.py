from rest_framework.serializers import ModelSerializer
from .models import User
from todoapp.serializers import ProjectModelSerializer
from rest_framework import serializers


class UserModelSerializer(ModelSerializer):
    project_set = ProjectModelSerializer(many=True)
    todo_set = serializers.HyperlinkedRelatedField(
        view_name="todo-detail",
        many=True,
        read_only=True,  # We can't create remark during creating user, it's illogical
    )

    # Commented this option, not sure, what is better
    # todo_set = ToDoModelSerializer(many=True, read_only=False)

    class Meta:
        model = User
        fields = (
            "id",
            'url',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_superuser',
            'project_set',
            'todo_set'
        )
