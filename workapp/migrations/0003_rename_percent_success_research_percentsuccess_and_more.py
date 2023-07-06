# Generated by Django 4.2 on 2023-07-06 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0002_leave_editable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='research',
            old_name='percent_success',
            new_name='percentSuccess',
        ),
        migrations.RenameField(
            model_name='research',
            old_name='publish_method',
            new_name='publishMethod',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='eduYear',
        ),
        migrations.AddField(
            model_name='research',
            name='publishDate',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='research',
            name='publishDb',
            field=models.CharField(default='', max_length=50),
        ),
    ]
