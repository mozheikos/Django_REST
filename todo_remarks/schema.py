import typing

from graphene import Schema, String, List, ObjectType, Mutation, ID, Field, Int
from graphene_django import DjangoObjectType
from usersapp.models import User
from todoapp.models import Project, ToDo


class UserType(DjangoObjectType):

    class Meta:
        model = User
        fields = '__all__'


class ProjectType(DjangoObjectType):

    class Meta:
        model = Project
        fields = '__all__'


class TODOType(DjangoObjectType):

    class Meta:
        model = ToDo
        fields = '__all__'


class Query(ObjectType):

    #  all
    all_users = List(UserType)
    all_projects = List(ProjectType)
    all_remarks = List(TODOType)

    # one
    me = Field(UserType)
    user_by_id = Field(UserType, pk=Int(required=False))
    project_by_id = Field(ProjectType, pk=Int(required=False))
    remark_by_id = Field(TODOType, pk=Int(required=False))

    # Users list
    @staticmethod
    def resolve_all_users(root, info) -> typing.List[User]:
        return User.objects.all()

    # Projects list
    @staticmethod
    def resolve_all_projects(root, info) -> typing.List[Project]:
        return Project.objects.all()

    # Remarks list
    @staticmethod
    def resolve_all_remarks(root, info) -> typing.List[ToDo]:
        return ToDo.objects.all()

    # get current authorized user
    @staticmethod
    def resolve_me(root, info) -> typing.Union[User, None]:
        user = info.context.user
        return user if user else None

    # get user by id
    @staticmethod
    def resolve_user_by_id(root, info, pk: int = None) -> typing.Union[User, None]:
        if pk:
            user = User.objects.filter(pk=pk).first()
            return user if user else None
        return None

    # get project by id (if authorized)
    @staticmethod
    def resolve_project_by_id(root, info, pk: int = None) -> typing.Union[Project, None]:
        # added this check because of permission settings for projects
        if info.context.user.is_authenticated:
            if pk:
                project = Project.objects.filter(pk=pk).first()
                return project if project else None
            return None
        return None


schema = Schema(query=Query)
