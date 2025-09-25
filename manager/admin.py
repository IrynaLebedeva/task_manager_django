from django.contrib import admin
from .models import Task, SubTask, Category

# Register your models here.
class SubTaskInlineAdmin(admin.TabularInline):
    model = SubTask
    extra = 2

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status','deadline', 'created_at')
    list_filter = ('status','categories')
    search_fields = ('title', 'status')
    ordering = ('-deadline',)
    inlines = [SubTaskInlineAdmin]


    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + '...'
        return obj.title
    short_title.short_description = 'Title'



@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status','deadline', 'created_at')
    list_filter = ('status','task')
    search_fields = ('title', 'status')
    ordering = ('-deadline',)

    @admin.action(description='Mark selected SubTasks as done')
    def mark_done(self, request, queryset):
        queryset.update(status='done')

    actions = ['mark_done']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)






