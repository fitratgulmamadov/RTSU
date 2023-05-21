from django import forms
from .models import Attendance


class AddAttendance(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'