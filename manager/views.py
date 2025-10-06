from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count,Q
from django.utils import timezone

from .models import Task
from .serializers import TaskSerializer


# Create your views here.
class TaskCreateView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['GET'])
    def stats(self, request):
        total_tasks = Task.objects.count()
        task_status = Task.objects.values('status').annotate(total=Count('id'))
        overdue_tasks = Task.objects.filter(Q(deadline__lt=timezone.now()) & ~Q(status='done')).count()

        return Response({'total_tasks': total_tasks,
                         'task_status': {item["status"]: item["total"] for item in task_status},
                         'overdue_tasks': overdue_tasks})



