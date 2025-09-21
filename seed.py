from datetime import timedelta
from django.utils import timezone
from manager.models import Task, SubTask

# task = Task.objects.create(title="Prepare presentation",
#                            description= "Prepare materials and slides for the presentation",
#                            status="new",
#                            deadline=timezone.now() + timedelta(days=3))
# SubTask.objects.create(title="Prepare presentation",
#                        description= "Find necessary information for the presentation",
#                        deadline=timezone.now() + timedelta(days=2),
#                        status="new",
#                        task=task)
# SubTask.objects.create(title="Create slides",
#                        description= "Create presentation slides",
#                        deadline=timezone.now() + timedelta(days=1),
#                        status="new",
#                        task=task)


for task in Task.objects.filter(status="new"):
    print(task.title, task.status)

for subtask in SubTask.objects.filter(status="done", deadline__lt=timezone.now()):
    print(subtask.title, subtask.deadline)

task1 = Task.objects.get(title="Prepare presentation")
task1.status = "in_progress"
task1.save()
# print(task1.status)

subtask=SubTask.objects.get(title="Gather information")
subtask.deadline=timezone.now()-timedelta(days=2)
subtask.save()
# print(subtask.deadline)

subtask1=SubTask.objects.get(title="Create slides")
subtask1.description="Create and format presentation slides"
subtask1.save()
# print(subtask1.description)

task2=Task.objects.get(title="Prepare presentation")
task2.subtasks.all().delete()
task2.delete()

