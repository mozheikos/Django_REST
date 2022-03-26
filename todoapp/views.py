from rest_framework.response import Response

from .models import Project, ToDo
from .serializers import ProjectModelSerializer, ToDoModelSerializer
from rest_framework.viewsets import ModelViewSet
from todoapp.filters import ProjectFilter, ToDoFilter
from django_filters import rest_framework as filters
from todoapp.paginators import ProjectListPagination, ToDOListPagination


class ProjectModelViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    pagination_class = ProjectListPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProjectFilter


class ToDoModelViewSet(ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoModelSerializer
    pagination_class = ToDOListPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ToDoFilter

    def destroy(self, request, pk=None, *args, **kwargs):
        obj = ToDo.objects.get(pk=pk)
        obj.status = "closed"
        obj.save()
        serializer = ToDoModelSerializer(obj, context={'request': request})
        return Response(data=serializer.data)
