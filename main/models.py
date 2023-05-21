# ./maim/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth.models import Permission

# group_lead_permissions = [
#     Permission.objects.get(name='Can change attendance'),
#     Permission.objects.get(name='Can view attendance')
# ]



class Faculty(models.Model):
    name = models.CharField(max_length=150)

    # __str__ для отображения строкового представления объекта
    def __str__(self) -> str:
        return self.name


class DeanUser(User):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    # берётся заводской метод создания пароля Для дальнейшего создания паролей по умолчанию
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'DeanUser'
        verbose_name_plural = 'DeanUsers'

class Cource(models.Model):
    name = models.IntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} курс {self.faculty}'
    
    def stst(self):
        return f'{self.name} курс {self.faculty}'

class Kafedra(models.Model):
    name = models.CharField(max_length=150)
    faculty = models.ForeignKey(Faculty, blank=True, null=True, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=150)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Descepline(models.Model):
    name = models.CharField(max_length=150)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,    
                                    verbose_name="Created by", 
                                    on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=150)
    group = models.ForeignKey('GroupSt', on_delete=models.DO_NOTHING)
    # faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    
    # def save(self, *args, **kwargs):
    #     self.faculty = self.group.cource.faculty

    def __str__(self):
        return self.name


class GroupSt(models.Model):
    name = models.CharField(max_length=150)
    desceplines = models.ManyToManyField(Descepline, null=True, blank=True)
    cource = models.ForeignKey(Cource, on_delete=models.CASCADE)
    # group_login = models.CharField(max_length=50)
    # group_password = models.CharField(max_length=500)    
    
    # def save(self, *args, **kwargs):    
    #     u = User.objects.create_user(
    #         username=self.group_login,
    #         password=make_password(self.group_password),
    #         is_staff=True)
    #     u.user_permissions.add(group_lead_permissions)
    #     return super().save(*args, **kwargs)


    # faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)


    # def save(self, *args, **kwargs):
    #     self.faculty = self.gr.cource.faculty



    def __str__(self):
        return f'{self.cource.name} {self.name} {self.cource.faculty}'



class Leader(User):
    group = models.ForeignKey(GroupSt, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'GroupLeader'
        verbose_name_plural = 'GroupLeaders'


class Lesson(models.Model):
    ORDER_CHOICES = ['Первая', 'Вторая', 'Третья']
    # перечисленное поле с валидаторами нижней границы и верхней границы
    order = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], choices=[(i, i) for i in range(6)])
    descepline = models.ForeignKey(Descepline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,    
                                    verbose_name="Created by", 
                                    on_delete=models.CASCADE)
    def kafedra(self):
        return self.teacher.kafedra

    def __str__(self):
        return f'{self.order}: {self.descepline.name}'


class Day(models.Model):
    DAY_CHOICES = [('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')]
    # текстовое поле или подающим списком
    day = models.CharField(max_length=10,
                  choices=DAY_CHOICES,
                  default='Monday')
    group = models.ForeignKey(GroupSt, on_delete=models.DO_NOTHING, blank=True, null=True)
    lessons = models.ManyToManyField(Lesson)
    status = models.BooleanField(default=True, verbose_name='Active or Inactive?')

    def __str__(self):
        return self.day


class Attendance(models.Model):

    today = models.DateField(auto_now_add=True)
    students = models.ForeignKey(Student, on_delete=models.CASCADE)
    was =  models.BooleanField(default=True, verbose_name='I')
    was2 = models.BooleanField(default=True, verbose_name='II')
    was3 = models.BooleanField(default=True, verbose_name='III')
    was4 = models.BooleanField(default=True, verbose_name='IV')
    was5 = models.BooleanField(default=True, verbose_name='V')
    gr = models.ForeignKey(GroupSt, on_delete=models.DO_NOTHING)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    # class Meta:
    #     permissions = (
    #         (f"can_edit_any", "Can edit any rentals"),
    #     )
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['students', 'today'], name='one_na_per_day')]

    # в дальнейшем для упрощения работы создаётся отдельное поле факультет
    def save(self, *args, **kwargs):
        self.gr = self.students.group
        self.faculty = self.gr.cource.faculty

        return super().save(*args, **kwargs)


    def __str__(self):
        return str(self.today)
    

class TimeTable(models.Model):
    group = models.ForeignKey(GroupSt, on_delete=models.CASCADE)
    days = models.ManyToManyField(Day)

    # возвращает список книг добавленных в расписании
    def get_days(self):
        return ', '.join([str(i) for i in self.days.all()])
    
    def __str__(self):
        return self.group.name

# для дальнейших перспектив бой создан модель журналов
class Journal(models.Model):
    group = models.ForeignKey(GroupSt, on_delete=models.CASCADE)
    time_table = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    attendance = models.ManyToManyField(Attendance)
    def __str__(self):
        return self.group.name

