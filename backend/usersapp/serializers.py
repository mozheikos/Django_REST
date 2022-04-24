from rest_framework.serializers import ModelSerializer
from .models import User
from todoapp.models import Project
from todoapp.serializers import ToDoModelSerializer
from rest_framework import serializers


class UserModelSerializer(ModelSerializer):

    project_set = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=Project.objects.all(),
        slug_field="title"
    )

    # todo_set = serializers.SlugRelatedField(
    #     slug_field="id",
    #     view_name="todo-detail",
    #     many=True,
    #     read_only=True,  # We can't create remark during creating user, it's illogical
    # )
    todo_set = ToDoModelSerializer(many=True)

    # Commented this option, not sure, what is better
    # todo_set = ToDoModelSerializer(many=True, read_only=False)

    class Meta:
        model = User
        fields = (
            "id",
            'username',
            'first_name',
            'last_name',
            'email',
            'project_set',
            'todo_set'
        )


class UserModelSerializerWithRole(UserModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            'username',
            'first_name',
            'last_name',
            'email',
            "is_superuser",
            "is_staff",
            'project_set',
            'todo_set'
        )
