# Generated by Django 3.1 on 2021-03-12 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('city', models.CharField(choices=[('Wrocław', 'Wroclaw'), ('Rzeszów', 'Rzeszow'), ('Inne', 'Inne')], default='Wrocław', max_length=11)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workstation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('workstation', models.CharField(choices=[('UXDesigner', 'Ux'), ('UIDesigner', 'Ui'), ('FrontEnd', 'Frontend'), ('BackEnd', 'Backend'), ('PHP', 'Php'), ('Python', 'Python'), ('React', 'React'), ('Mobile', 'Mobile'), ('ScrumMaster', 'Scrummaster'), ('VUE', 'Vue')], default='UXDesigner', max_length=11)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]