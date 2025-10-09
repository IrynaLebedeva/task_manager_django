from sqlite3.dbapi2 import apilevel

from rest_framework import viewsets, generics
from rest_framework.decorators import action, api_view
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

# class TaskListView(generics.ListAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
@api_view(['Get'])
def get_tasks_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

 # class TaskGetDetailView(generics.RetrieveAPIView):
 #    queryset = Task.objects.all()
 #    serializer_class = TaskSerializer

@api_view(['Get'])
def get_tasks_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    serializer = TaskSerializer(task)
    return Response(serializer.data)

