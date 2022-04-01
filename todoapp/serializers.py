from usersapp.models import User
from .models import Project, ToDo
from rest_framework import serializers


class ProjectModelSerializer(serializers.ModelSerializer):
    # users = serializers.HyperlinkedRelatedField(  # HyperLinkRelatedField for quick transfer to users page
    #     view_name="user-detail",
    #     many=True,
    #     read_only=False,
    #     queryset=User.objects.all(),
    # )

    class Meta:
        model = Project
        fields = ("id", "title", "url", "users", "repository_link",)


class ToDoModelSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(  # It can be HyperLinkRelatedField, but can be not, as designer will say
        read_only=False,
        queryset=User.objects.all(),
        slug_field='username'
    )

    project = serializers.SlugRelatedField(  # It can be HyperLinkRelatedField, but can be not, as designer will say
        read_only=False,
        queryset=Project.objects.all(),
        slug_field='title'
    )

    status = serializers.ChoiceField(choices=ToDo.STATUS_CHOICES, )

    class Meta:
        model = ToDo
        fields = ("user", "project", "url", "text", "created_at", "updated_at", "status")
