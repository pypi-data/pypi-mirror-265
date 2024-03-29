from django_q.models import Task
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from energy_base.q_api.filters import TaskFilterSet
from energy_base.api.permissions import IsSuperUser
from energy_base.q_api.serializers import TaskSerializer


@extend_schema(tags=['admin/tasks'])
class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsSuperUser]
    filterset_class = TaskFilterSet

