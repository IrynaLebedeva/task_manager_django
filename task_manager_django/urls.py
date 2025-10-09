"""
URL configuration for task_manager_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from manager.views import TaskCreateView
from manager import views

router = DefaultRouter()
router.register(r'task', TaskCreateView, basename='task')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/v1/tasks/', views.get_tasks_list, name='tasks_list'),
    path('api/v1/tasks/<int:pk>', views.get_tasks_detail, name='tasks_detail'),
]
