# Generated by Django 4.2.1 on 2023-05-17 13:37

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('today', models.DateField(auto_now_add=True)),
                ('was', models.BooleanField(default=True, verbose_name='I')),
                ('was2', models.BooleanField(default=True, verbose_name='II')),
                ('was3', models.BooleanField(default=True, verbose_name='III')),
                ('was4', models.BooleanField(default=True, verbose_name='IV')),
                ('was5', models.BooleanField(default=True, verbose_name='V')),
            ],
        ),
        migrations.CreateModel(
            name='Cource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], default='Monday', max_length=10)),
                ('status', models.BooleanField(default=True, verbose_name='Active or Inactive?')),
            ],
        ),
        migrations.CreateModel(
            name='Descepline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='GroupSt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('cource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cource')),
                ('desceplines', models.ManyToManyField(blank=True, null=True, to='main.descepline')),
            ],
        ),
        migrations.CreateModel(
            name='Kafedra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.ManyToManyField(to='main.day')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.groupst')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('kafedra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.kafedra')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.groupst')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('descepline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.descepline')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Leader',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.groupst')),
            ],
            options={
                'verbose_name': 'GroupLeader',
                'verbose_name_plural': 'GroupLeaders',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.ManyToManyField(to='main.attendance')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.groupst')),
                ('time_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.timetable')),
            ],
        ),
        migrations.AddField(
            model_name='descepline',
            name='kafedra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.kafedra'),
        ),
        migrations.CreateModel(
            name='DeanUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.faculty')),
            ],
            options={
                'verbose_name': 'DeanUser',
                'verbose_name_plural': 'DeanUsers',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='day',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.groupst'),
        ),
        migrations.AddField(
            model_name='day',
            name='lessons',
            field=models.ManyToManyField(to='main.lesson'),
        ),
        migrations.AddField(
            model_name='cource',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.faculty'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.faculty'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='gr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.groupst'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='students',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student'),
        ),
    ]
