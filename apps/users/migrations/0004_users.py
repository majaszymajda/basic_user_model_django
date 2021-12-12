# Generated by Django 3.1 on 2021-04-01 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_places'),
        ('core_users', '0003_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_leader',
        ),
        migrations.RemoveField(
            model_name='user',
            name='modification_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='work_city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='workstations',
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=True)),
                ('is_leader', models.BooleanField(default=True)),
                ('modification_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('work_city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='places.city')),
                ('workstations', models.ManyToManyField(related_name='workstations', to='places.Workstation')),
            ],
        ),
    ]