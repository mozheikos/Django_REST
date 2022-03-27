from .models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from django.http import JsonResponse
from .serializers import UserModelSerializer
# from rest_framework.pagination import LimitOffsetPagination

#
# class UsersCustomPaginator(LimitOffsetPagination):
#     default_limit = 100


class UserModelViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # pagination_class = UsersCustomPaginator


def get_links(request):
    """Пока это находится здесь, в дальнейшем можно будет модернизировать и перенести в какое-то другое приложение,
    где это будет более уместно, также в ответ сервера к каждой ссылке можно будет добавить URL"""
    links = ['Все пользователи', "Проекты", "TODO-листы"]
    return JsonResponse({'links': links})
