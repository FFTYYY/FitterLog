# Generated by Django 3.0.3 on 2020-07-28 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0021_auto_20200728_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='config',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='experiment.ProjectConfig'),
        ),
    ]