from .models import User
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse

from .serializers import UserModelSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


def get_links(request):
    """Пока это находится здесь, в дальнейшем можно будет модернизировать и перенести в какое-то другое приложение,
    где это будет более уместно, также в ответ сервера к каждой ссылке можно будет добавить URL"""
    links = ['Все пользователи', "Проекты", "TODO-листы"]
    return JsonResponse({'links': links})
