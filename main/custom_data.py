from .models import *


class FormatData:
    def __init__(self) -> None:
        self.att = Attendance.objects.all()
        self.groups = GroupSt.objects.all()
        self.students = Student.objects.all()
        self.timetable = TimeTable.objects.all()
    
    def get(self):
        return {group: 
                 [{'name': student, 
                   'att': {attend.today.strftime("%b %d"): int(not attend.was) + int(not attend.was2)+ int(not attend.was3) + int(not attend.was4)+ int(not attend.was5) for attend in self.att if student == attend.students}
                   } for student in self.students if student.group == group]
                  for group in self.groups}
