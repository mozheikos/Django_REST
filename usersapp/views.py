from .models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from django.http import JsonResponse
from .serializers import UserModelSerializer
from rest_framework.pagination import LimitOffsetPagination


class UserModelViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet
):

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    pagination_class = LimitOffsetPagination


def get_links(request):
    """Пока это находится здесь, в дальнейшем можно будет модернизировать и перенести в какое-то другое приложение,
    где это будет более уместно, также в ответ сервера к каждой ссылке можно будет добавить URL"""
    links = [
        {"verbose_name": "Все пользователи", "link": "/users"},
        {"verbose_name": "Проекты", "link": "/projects"},
        {"verbose_name": "TODO-листы", "link": "/ToDo"},
    ]
    return JsonResponse({'links': links})
