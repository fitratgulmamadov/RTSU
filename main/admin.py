#./main/admin.py

from typing import Any, Dict, Type
from django.contrib import admin
import datetime
from django.contrib.admin.options import ModelAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from .filters import DesceplineFilter, GroupFilter
from .models import *



# Регистрация моделей с помощю декоратора @admin.register


# регистрация модели Day
@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    # список колонок отображаемых в админке, список фильтров, список изменяемых колонок
    list_display = ('day', 'group', 'get_lessons', 'status' )
    # добавляется собственный фильтр для ролевого разделения
    list_filter = ["day", GroupFilter,  'status']
    list_editable = ('status', )

    # добавление действий в админ панели
    def make_action(self, quality):
        name = f'action_{quality}_{quality.group.name}'
        action = lambda modeladmin, req, qset: [quality.days.add(i) for i in qset]
        return (name, (action, name, f"Add to {quality} of {quality.group.cource}"))
    
    # возврат списка действий доступных из админке
    def get_actions(self, request):
        return dict([self.make_action(q) for q in TimeTable.objects.all()])
    

    def get_lessons(self, obj):
        lesns = obj.lessons.all()
        return ', '.join(str(i).split(':')[1] for i in lesns)
    
    get_lessons.short_description = "Lessons"

    # псевдоразделения ролей
    def get_queryset(self, request):
        query = super(DayAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(group__cource__faculty=DeanUser.objects.get(id=request.user.id).faculty)

    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            context['adminform'].form.fields['lessons'].queryset = Lesson.objects.filter(created_by=request.user)
            context['adminform'].form.fields['group'].queryset = GroupSt.objects.filter(cource__faculty=DeanUser.objects.get(id=request.user.id).faculty)
        
        return super(DayAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_filter = ["days", GroupFilter]
    list_display = ('group', 'get_days' )
    
    # ограничение выпадающего списка по пользователю
    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            context['adminform'].form.fields['group'].queryset = GroupSt.objects.filter(cource__faculty=DeanUser.objects.get(id=request.user.id).faculty)
            context['adminform'].form.fields['days'].queryset = Day.objects.filter(group__cource__faculty=DeanUser.objects.get(id=request.user.id).faculty)
        return super(TimeTableAdmin, self).render_change_form(request, context, *args, **kwargs)

    def get_queryset(self, request):
        query = super(TimeTableAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(group__cource__faculty=DeanUser.objects.get(id=request.user.id).faculty)



@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('order', 'descepline', 'teacher', 'kafedra')
    list_filter = ('order', DesceplineFilter, 'teacher')
    exclude = ('created_by', )
    list_display_links = list_display

    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            context['adminform'].form.fields['descepline'].queryset = Descepline.objects.filter(created_by=request.user.id)
        return super(LessonAdmin, self).render_change_form(request, context, *args, **kwargs)

    def get_queryset(self, request):
        query = super(LessonAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(descepline__created_by=request.user)

    def make_action(self, quality):
        name = f'action_{quality}_{quality.group.name}'
        action = lambda modeladmin, req, qset: [quality.lessons.add(i) for i in qset]
        return (name, (action, name, f"Add to {quality} of {quality.group.name}"))

    def get_actions(self, request):
        return dict([self.make_action(q) for q in Day.objects.all()])

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = ['students', 'today', 'was', 'was2', 'was3', 'was4', 'was5', 'gr'] 
    list_editable = ['was', 'was2', 'was3', 'was4', 'was5']
    #datetime.datetime.today().weekday()
    # исключается поля группа и факультет

    exclude = ('gr', 'faculty')

    # def get_list_editable(self, request):
    #     if request.user.is_superuser:
    #         return ['was', 'was2', 'was3', 'was4', 'was5']
    #     else:

    #         from datetime import datetime
    #         days = [('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')]
    #         # today = [days for i in range(len(days)) if i == datetime.now().weekday()]
            
    #         # print(Day.objects.get(group = Leader.objects.get(id=request.user.id).group, day=today))
    #         return

        

    def changelist_view(self, request, extra_context=None):
        self.list_editable = self.get_list_editable(request)
        return super().changelist_view(request, extra_context)
    
    # переписывается ранее созданный фильтр из-за того что в названии не совпадает переменная
    class GroupFilter_cust(GroupFilter):
        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(gr=self.value())

    list_filter = ('today', GroupFilter_cust)
           
    def get_queryset(self, request):
        query = super(AttendanceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query.all()
        try:
            return query.filter(gr=Leader.objects.get(id=request.user.id).group, today=datetime.datetime.now()) 
        except:
            return query.filter(faculty=DeanUser.objects.get(id=request.user.id).faculty) 


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_filter = ('kafedra', )
    list_display = ('name', 'kafedra')

    def custom_filter(self, request):
        return Lesson.objects.filter(descepline__created_by=request.user)


@admin.register(Descepline)
class DesceplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'kafedra')
    exclude = ('created_by', )

    def get_queryset(self, request):
        query = super(DesceplineAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(created_by=request.user)
    
    # переписывается метод save_model для определения владельца
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'group')
    list_filter = (GroupFilter,)
    exclude = ('faculty', )

    def make_action(self, quality):
        name = f'action_{quality}'
        action = lambda modeladmin, req, qset: [Attendance(students=i).save() for i in qset if i not in [_.students for _ in Attendance.objects.filter(today=datetime.datetime.today())]]
        return (name, (action, name, f"EXPORT TO ATTENDANCE"))

    def get_actions(self, request):
        return dict([self.make_action('arg')])
    
    def get_queryset(self, request):
        query = super(StudentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(group__cource__faculty=DeanUser.objects.get(id=request.user.id).faculty)
    
    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            context['adminform'].form.fields['group'].queryset = GroupSt.objects.filter(cource__faculty= DeanUser.objects.get(id=request.user.id).faculty)
        return super(StudentAdmin, self).render_change_form(request, context, *args, **kwargs)





@admin.register(Cource)
class CourceAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        query = super(CourceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(faculty=DeanUser.objects.get(id=request.user.id).faculty) 
    
    
    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            context['adminform'].form.fields['faculty'].queryset = Faculty.objects.filter(id=DeanUser.objects.get(id=request.user.id).faculty.id    )
        return super(CourceAdmin, self).render_change_form(request, context, *args, **kwargs)






@admin.register(GroupSt)
class GroupStAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        query = super(GroupStAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(cource__faculty=DeanUser.objects.get(id=request.user.id).faculty)

    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            context['adminform'].form.fields['desceplines'].queryset = Descepline.objects.filter(created_by=request.user.id)
            context['adminform'].form.fields['cource'].queryset = Cource.objects.filter(faculty=DeanUser.objects.get(id=request.user.id).faculty)  
        return super(GroupStAdmin, self).render_change_form(request, context, *args, **kwargs)


#  Дефолтная регистрация моделей

admin.site.register([Kafedra , Leader, DeanUser, Faculty])