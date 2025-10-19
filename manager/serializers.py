from datetime import timezone

from rest_framework import serializers

from .models import Task, Category, SubTask


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'deadline')
        read_only_fields = ('id', 'created_at')

class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubTask
        fields = ('id', 'title', 'task', 'deadline','created_at')


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category with this name already exists")
        return value

    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError("Category with this name already exists")
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        new_name = validated_data.get('name', instance.name)
        if Category.objects.filter(name__iexact=new_name).exclude(id=instance.id).exists():
            raise serializers.ValidationError("Category with this name already exists")
        instance.name = new_name
        instance.save()
        return instance

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'status', 'deadline', 'created_at')

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks')

class TaskCreateSerializer(serializers.ModelSerializer):
    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past")
        return value
