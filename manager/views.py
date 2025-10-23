from sqlite3.dbapi2 import apilevel
from rest_framework.views import status
from rest_framework import viewsets, generics
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from django.db.models import Count,Q
from django.utils import timezone
from datetime import datetime
from rest_framework.views import APIView
from .pagination import SubTaskPagination

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskCreateSerializer


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

# class SubTaskListCreateView(APIView):
#
#     def get(self, request):
#         subtasks = SubTask.objects.all()
#         serializer = SubTaskCreateSerializer(subtasks, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "SubTask not found"}, status=404)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)


    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "SubTask not found"}, status=404)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({"error": "SubTask not found"}, status=404)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskByDayView(APIView):
    def get(self, request):
        day = request.query_params.get('day', None)
        tasks = Task.objects.all()

        if day:
            day = day.lower()
            tasks = [task for task in tasks if task.deadline.strftime('%A').lower() == day]

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubTaskListCreateView(ListCreateAPIView):

    queryset = SubTask.objects.all().order_by('-created_at')
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination

# class SubTaskFilterView(ListCreateAPIView):
#
#     serializer_class = SubTaskCreateSerializer
#     pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')

        task_name = self.request.query_params.get('task_name', None)
        status = self.request.query_params.get('status', None)
        if task_name:
            queryset = queryset.filter(task__title__icontains=task_name)
        if status:
            queryset = queryset.filter(status__iexact=status)

        return queryset






