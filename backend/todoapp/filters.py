from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget

from todoapp.models import Project, ToDo
from usersapp.models import User


class ProjectFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='contains')
    users = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ["title", "users"]


class ToDoFilter(filters.FilterSet):
    project = filters.ModelChoiceFilter(queryset=Project.objects.all())
    created_at = filters.DateFromToRangeFilter(widget=RangeWidget(attrs={"type": "date"}))

    class Meta:
        model = ToDo
        fields = ['project', "created_at"]
