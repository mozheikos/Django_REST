from rest_framework.pagination import LimitOffsetPagination


class ProjectListPagination(LimitOffsetPagination):
    default_limit = 10


class ToDOListPagination(LimitOffsetPagination):
    default_limit = 20
