from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ['name', 'date_start', 'date_end', 'status']


@admin.register(Dolzn)
class DolznAdmin(ModelAdmin):
    list_display = ['name']


@admin.register(AdvUser)
class AdvUserAdmin(ModelAdmin):
    list_display = ['username', 'dolzn']


@admin.register(TypeWork)
class TypeWorkAdmin(ModelAdmin):
    list_display = ['name']


@admin.register(WorkOnProject)
class WorkOnProjectAdmin(ModelAdmin):
    list_display = ['project', 'worker', 'description', 'type_work', 'dat']


admin.site.register(WorkerInProject)

