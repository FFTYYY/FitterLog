# Generated by Django 3.0.3 on 2020-05-04 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0013_experimentgroup_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupconfig',
            name='show_order',
            field=models.TextField(default=''),
        ),
    ]
