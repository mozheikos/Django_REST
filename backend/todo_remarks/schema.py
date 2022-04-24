import typing

from graphene import Schema, String, List, ObjectType, Mutation, ID, Field, Int, Boolean, Enum
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from usersapp.models import User
from todoapp.models import Project, ToDo


# Definition of filtering criteria
class Sign(Enum):
    EQ = 0
    LT = 1
    GT = 2
    LTE = 3
    GTE = 4
    CONTAINS = 5


# Using raw query for filter, it takes possibility to get variety in filtering to frontend
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
        sign=Sign(required=True),
        value=String(required=False)
    )
    projects_filtered = List(
        ProjectType,
        field=String(required=True),
        sign=Sign(required=True),
        value=String(required=False)
    )
    remarks_filtered = List(
        TODOType,
        field=String(required=True),
        sign=Sign(required=True),
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
        # add pagination as possible
        start = paginate_by * (page - 1)
        end = start + paginate_by
        return users[start:end]

    # Projects list
    @staticmethod
    def resolve_all_projects(root, info, page: int = None, paginate_by: int = 10) -> typing.List[Project]:
        projects = Project.objects.all().order_by("id")
        if not page:
            return projects
        # add pagination as possible
        start = paginate_by * (page - 1)
        end = start + paginate_by
        return projects[start:end]

    # Remarks list
    @staticmethod
    def resolve_all_remarks(root, info, page: int = None, paginate_by: int = 10) -> typing.List[ToDo]:
        remarks = ToDo.objects.all().order_by("id")
        if not page:
            return remarks
        # add pagination as possible
        start = paginate_by * (page - 1)
        end = start + paginate_by
        return remarks[start:end]

    # get current authorized user
    @staticmethod
    def resolve_me(root, info) -> typing.Union[User, None]:
        user = info.context.user
        return user if user else GraphQLError(message=f'You are not authorized')

    # get user by id
    @staticmethod
    def resolve_user_by_id(root, info, pk: int = None) -> typing.Union[User, GraphQLError]:
        if pk:
            user = User.objects.filter(pk=pk).first()
            return user if user else GraphQLError(message=f'User with {pk=} do not exists')
        return GraphQLError(message='"pk" value is required')

    # get project by id (if authorized)
    @staticmethod
    def resolve_project_by_id(root, info, pk: int = None) -> typing.Union[Project, GraphQLError]:
        # added this check because of permission settings for projects
        if info.context.user.is_authenticated:
            if pk:
                project = Project.objects.filter(pk=pk).first()
                return project if project else GraphQLError(message=f'Project with {pk=} do not exists')
            return GraphQLError(message='"pk" value is required')
        return GraphQLError(message=f'You are not authorized')

    # get remark by id
    @staticmethod
    def resolve_remark_by_id(root, info, pk: int = None) -> typing.Union[ToDo, GraphQLError]:
        if pk:
            remark = ToDo.objects.filter(pk=pk).first()
            return remark if remark else GraphQLError(message=f'Remark with {pk=} do not exists')
        return GraphQLError(message='"pk" value is required')

    # get users list by filter
    @staticmethod
    def resolve_users_filtered(root, info, field: str, sign: int, value: str = None):
        allowed_signs = ("=", '<', '>', '<=', '>=', 'like')
        sign = allowed_signs[sign]
        if value:
            sql = get_query(table_name="usersapp_user", field=field, sign=sign, value=value)

            users = User.objects.raw(
                raw_query=sql
            )
            return users
        return User.objects.all()

    # get projects list by filter
    @staticmethod
    def resolve_projects_filtered(root, info, field: str, sign: int, value: str = None):
        allowed_signs = ("=", '<', '>', '<=', '>=', 'like')
        sign = allowed_signs[sign]
        if value:
            sql = get_query(table_name="todoapp_project", field=field, sign=sign, value=value)

            projects = Project.objects.raw(
                raw_query=sql
            )
            return projects
        return Project.objects.all()

    # get remarks list by filter
    @staticmethod
    def resolve_remarks_filtered(root, info, field: str, sign: int, value: str = None):
        allowed_signs = ("=", '<', '>', '<=', '>=', 'like')
        sign = allowed_signs[sign]
        if value:
            sql = get_query(table_name="todoapp_todo", field=field, sign=sign, value=value)

            remarks = ToDo.objects.raw(
                raw_query=sql
            )
            return remarks
        return ToDo.objects.all()


# Mutations
class UserUpdateMutation(Mutation):

    class Arguments:
        pk = ID(required=True)
        username = String()
        first_name = String()
        last_name = String()
        email = String()

    user = Field(UserType)

    @classmethod
    def mutate(cls, root, info, pk: int, **kwargs):
        # updating allows to authorized users (for updating own info) and to staff (to updating all users)
        if info.context.user.id == pk or info.context.user.is_staff:
            User.objects.filter(pk=pk).update(**kwargs)
            user = User.objects.get(pk=pk)
            return UserUpdateMutation(user=user)
        return GraphQLError(message=f'You are not authorized')


class UserDeleteMutation(Mutation):

    class Arguments:
        pk = ID(required=True)

    user = Field(UserType)

    @classmethod
    def mutate(cls, root, info, pk: int):
        # deleting allows to authorized users (for deleting own account) and to staff (to updating all users)
        if not info.context.user.is_authenticated:
            return GraphQLError(message=f'You are not authorized')
        if info.context.user.id == pk or info.context.user.is_staff:
            if info.context.user.is_staff:
                user = User.objects.filter(pk=pk).first()
                if user:
                    user.is_active = False
                    user.save()
                    user.refresh_from_db()
                    return UserDeleteMutation(user=user)
                return GraphQLError(message=f"User with {pk=} do not exists")
            else:
                User.objects.filter(pk=pk).delete()
                return None
        else:
            return GraphQLError(message=f'Permission denied')


class UserActivateMutation(Mutation):

    class Arguments:
        pk = ID(required=True)

    user = Field(UserType)

    @classmethod
    def mutate(cls, root, info, pk: int):
        # activate allows only for staff
        if info.context.user.is_staff:
            user = User.objects.filter(pk=pk).first()
            if user:
                user.is_active = True
                user.save()
                user.refresh_from_db()
                return UserDeleteMutation(user=user)
            return GraphQLError(message=f"User with {pk=} do not exists")

        else:
            return GraphQLError(message=f'Permission denied')


class RemarkCreateMutation(Mutation):

    class Arguments:
        project_id = Int(required=True)
        text = String(required=True)

    remark = Field(TODOType)

    @classmethod
    def mutate(cls, root, info, project_id: int, text: str):
        # remarks can create only authorized users
        if not info.context.user.is_authenticated:
            return GraphQLError(message=f'You are not authorized')

        project = Project.objects.filter(pk=project_id).first()
        # user can create remark only for existing project
        if not project:
            return GraphQLError(message=f'Project with {project_id=} do not exists')

        project_users = project.users.select_related()
        user_id = info.context.user.id
        user = User.objects.get(pk=user_id)

        # User can create remark for project if related
        if user in project_users:
            remark = ToDo.objects.create(project=project, user=user, text=text)
            return RemarkCreateMutation(remark=remark)
        return GraphQLError(message=f"You can't create remark for this project")


class Mutations(ObjectType):
    update_user = UserUpdateMutation.Field()
    delete_user = UserDeleteMutation.Field()
    activate_user = UserActivateMutation.Field()
    create_remark = RemarkCreateMutation.Field()


schema = Schema(query=Query, mutation=Mutations)
