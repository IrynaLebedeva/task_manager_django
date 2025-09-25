from django.db import models
from django.utils import timezone


# Create your models here.
STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    class Meta:
        db_table = 'task_manager_category'
        verbose_name =  'Category'
        verbose_name_plural = 'Categories'
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_category_name')]


    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100, unique=True, unique_for_date='created_at', verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание задачи', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='tasks', verbose_name='Категория')
    status =  models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус задачи')
    deadline = models.DateTimeField(verbose_name='Дата и время дедлайн')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    class Meta:
        db_table = 'task_manager_task'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['title'], name='unique_task_title')]

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название подзадачи')
    description = models.TextField(verbose_name='Описание подзадачи',blank=True,null=True)
    task = models.ForeignKey(Task, on_delete=models.PROTECT, null=True, related_name='subtasks', verbose_name='Основная задача')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус задачи')
    deadline = models.DateTimeField(verbose_name='Дата и время дедлайн')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['title'], name='unique_subtask_title')]

    def __str__(self):
        return f"подзадача {self.title}"










