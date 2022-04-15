import typing

from graphene import Schema, String, List, ObjectType, Mutation, ID, Field, Int, Boolean
from graphene_django import DjangoObjectType
from usersapp.models import User
from todoapp.models import Project, ToDo


def get_query(table_name: str, field: str, sign: str, value: str = None) -> str:
    if sign == "like":
        add_sign = '%'
    else:
        add_sign = ""

    sql = f'''
        select * from {table_name}
        where {field} {sign} \'{add_sign}{value}{add_sign}\'
    '''
    return sql


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
    all_users = List(
        UserType,
        page=Int(required=False),
        paginate_by=Int(required=False)
    )
    all_projects = List(
        ProjectType,
        page=Int(required=False),
        paginate_by=Int(required=False)
    )
    all_remarks = List(
        TODOType,
        page=Int(required=False),
        paginate_by=Int(required=False)
    )

    # filtered
    users_filtered = List(
        UserType,
        field=String(required=True),
        sign=String(required=True),
        value=String(required=False)
    )
    projects_filtered = List(
        ProjectType,
        field=String(required=True),
        sign=String(required=True),
        value=String(required=False)
    )
    remarks_filtered = List(
        TODOType,
        field=String(required=True),
        sign=String(required=True),
        value=String(required=False)
    )

    # one
    me = Field(UserType)
    user_by_id = Field(UserType, pk=Int(required=False))
    project_by_id = Field(ProjectType, pk=Int(required=False))
    remark_by_id = Field(TODOType, pk=Int(required=False))

    # Users list
    @staticmethod
    def resolve_all_users(root, info, page: int = None, paginate_by: int = 10) -> typing.List[User]:
        users = User.objects.all().order_by('id')
        if not page:
            return users
        start = paginate_by * (page - 1)
        end = start + paginate_by
        return users[start:end]

    # Projects list
    @staticmethod
    def resolve_all_projects(root, info, page: int = None, paginate_by: int = 10) -> typing.List[Project]:
        projects = Project.objects.all().order_by("id")
        if not page:
            return projects
        start = paginate_by * (page - 1)
        end = start + paginate_by
        return projects[start:end]

    # Remarks list
    @staticmethod
    def resolve_all_remarks(root, info, page: int = None, paginate_by: int = 10) -> typing.List[ToDo]:
        remarks = ToDo.objects.all().order_by("id")
        if not page:
            return remarks
        start = paginate_by * (page - 1)
        end = start + paginate_by
        return remarks[start:end]

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

    # get remark by id
    @staticmethod
    def resolve_remark_by_id(root, info, pk: int = None) -> typing.Union[ToDo, None]:
        if pk:
            remark = ToDo.objects.filter(pk=pk).first()
            return remark if remark else None
        return None

    # get users list by filter
    @staticmethod
    def resolve_users_filtered(root, info, field: str, sign: str, value: str = None):

        if value:
            sql = get_query(table_name="usersapp_user", field=field, sign=sign, value=value)

            users = User.objects.raw(
                raw_query=sql
            )
            return users
        return User.objects.all()

    # get projects list by filter
    @staticmethod
    def resolve_projects_filtered(root, info, field: str, sign: str, value: str = None):

        if value:
            sql = get_query(table_name="todoapp_project", field=field, sign=sign, value=value)

            projects = Project.objects.raw(
                raw_query=sql
            )
            return projects
        return Project.objects.all()

    # get remarks list by filter
    @staticmethod
    def resolve_remarks_filtered(root, info, field: str, sign: str, value: str = None):

        if value:
            sql = get_query(table_name="todoapp_todo", field=field, sign=sign, value=value)

            remarks = ToDo.objects.raw(
                raw_query=sql
            )
            return remarks
        return ToDo.objects.all()


schema = Schema(query=Query)
