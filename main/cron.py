from .models import Kafedra


def my_scheduled_job():
    Kafedra.objects.create(name='my_scheduled_job')