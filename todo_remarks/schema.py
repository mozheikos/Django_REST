from graphene import Schema, String, List, ObjectType, Mutation, ID
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

    @staticmethod
    def resolve_all_users(root, info):
        return User.objects.all()

    @staticmethod
    def resolve_all_projects(root, info):
        return Project.objects.all()

    @staticmethod
    def resolve_all_remarks(root, info):
        return ToDo.objects.all()


schema = Schema(query=Query)
