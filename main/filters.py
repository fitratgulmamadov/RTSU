from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import *

class DesceplineFilter(admin.SimpleListFilter):

    title = 'Descepline'
    parameter_name = 'descepline'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [(i.id, i.name) for i in Descepline.objects.all()]
        return [(i.id, i.name) for i in Descepline.objects.filter(created_by=request.user.id)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(descepline=self.value())
        

class GroupFilter(admin.SimpleListFilter):

    title = 'Group'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [(i.id, i) for i in GroupSt.objects.all()]
        try:
            return [(i.id, i) for i in GroupSt.objects.filter(cource__faculty= DeanUser.objects.get(id=request.user.id).faculty)]
        except:
            pass

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(group=self.value())

        
