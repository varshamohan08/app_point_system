# Generated by Django 5.1 on 2024-08-16 00:18

import tasks_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetails',
            name='screenshot',
            field=models.ImageField(upload_to=tasks_app.models.upload_to),
        ),
    ]
