# Generated by Django 3.0.3 on 2020-07-28 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0020_project_config_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_files', models.TextField(default='')),
                ('cmd_pref', models.CharField(default='', max_length=50)),
                ('cmd_comm', models.CharField(default='', max_length=50)),
                ('cmd_entr', models.CharField(default='', max_length=50)),
                ('cmd_suff', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='config_files',
        ),
        migrations.AddField(
            model_name='project',
            name='config',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='experiment.ProjectConfig'),
        ),
    ]