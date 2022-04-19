from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, ToDo
from .serializers import ProjectModelSerializer, ToDoModelSerializer
from rest_framework.viewsets import ModelViewSet
from todoapp.filters import ProjectFilter, ToDoFilter
from django_filters import rest_framework as filters
from todoapp.paginators import ProjectListPagination, ToDOListPagination
from usersapp.models import User


class ProjectModelViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    pagination_class = ProjectListPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProjectFilter
    # permission_classes = [IsAuthenticated]

    def update(self, request, pk=None, *args, **kwargs):
        return super(ProjectModelViewSet, self).update(request=request, pk=pk, partial=True, *args, **kwargs)


class ToDoModelViewSet(ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoModelSerializer
    pagination_class = ToDOListPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ToDoFilter

    def create(self, request, *args, **kwargs):
        project = Project.objects.get(pk=int(request.data["project"]))
        user = User.objects.get(pk=int(request.data["user"]))
        obj = ToDo.objects.create(user=user, project=project, text=request.data["text"])
        obj.save()
        serializer = ToDoModelSerializer(obj, context={"request": request})
        return Response(data=serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        return super(ToDoModelViewSet, self).update(request=request, pk=pk, partial=True, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        obj = ToDo.objects.get(pk=pk)
        obj.status = "closed"
        obj.save()
        serializer = ToDoModelSerializer(obj, context={'request': request})
        return Response(data=serializer.data)
