from django.shortcuts import render
from .models import *
from datetime import datetime
from .forms import AddAttendance
from .custom_data import FormatData
from django.views.generic import TemplateView
import calendar
from rest_framework import viewsets 
from .serializers import AttendanceSerializer, StudentSerializer 
from django.forms.models import inlineformset_factory
from django.http import JsonResponse

class AttendanceView(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer




def attendance(request):
    data = FormatData().get()
    print(request.GET)
    param_dict = request.GET
    faculties = Faculty.objects.all()
    groups = GroupSt.objects.all()
    cources = Cource.objects.all()
    show_calendar = [_day.strftime("%b %d") for _day in calendar.Calendar().itermonthdates(2023, datetime.now().month)]
    # show_calendar = [i. for i in show_calendar]
    # today_index = show_calendar.ind   ex(datetime.now().date())

    if 'group' in param_dict:
        return render(request, 'index.html', {'p' : 'att', 'data': data[GroupSt.objects.get(id=int(param_dict['group']))], 'calendar': show_calendar, 'faculties': faculties, 'groups': groups, 'cources': cources})
    

    # show_calendar = show_calendar[today_index - 7: today_index] + show_calendar[today_index: today_index + 7]
    # print(data)
    return render(request, 'index.html', {'p' : 'att','data': data, 'calendar': show_calendar, 'faculties': faculties, 'groups': groups, 'cources': cources})


def timetable(request):
    print(request.GET)
    param_dict = request.GET
    faculties = Faculty.objects.all()
    groups = GroupSt.objects.all()
    cources = Cource.objects.all()
    if 'group' in param_dict:
        timetable = TimeTable.objects.get(group__id=param_dict['group'])
    else:
        return render(request, 'index1.html', {'p' : 'groups','faculties': faculties, 'groups': groups, 'cources': cources})  
    # formater(timetable)
    # return JsonResponse(formater(timetable))
    return render(request, 'index1.html', {'p' : 'groups','faculties': faculties, 'groups': groups, 'cources': cources, 'data': report_formater(timetable)})

def report_formater(obj):
    ret = {
        'name': obj.group.name,
        'days': []
        }
    for i in obj.days.all():
        tmp = []
        for j in  i.lessons.all():
            tmp.append({'order': j.order, 'name':  j.descepline.name, 'teacher': j.teacher.name})
        ret['days'].append({'name': i.day,
                            'data': tmp})
    return ret       




# def today_weekday():
#     week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     today_weekd = week[datetime.today().weekday()]
#     today_weekd = week[0]
#     return Day.objects.filter(day=today_weekd)

