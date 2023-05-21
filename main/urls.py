from django.urls import path, include
from .views import attendance, timetable

from rest_framework import routers
from .views import AttendanceView, StudentView


router = routers.DefaultRouter()
router.register(r"attendance", AttendanceView)
router.register(r"students", StudentView)


urlpatterns = [
    path('', attendance, name='att'),
    path("api/", include(router.urls)),
    path('qq/', timetable, name='groups')

]
