# Generated by Django 4.2 on 2023-05-27 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0007_rename_personnel_command_recorder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='research',
            old_name='personnel',
            new_name='recorder',
        ),
        migrations.RenameField(
            model_name='socialservice',
            old_name='personnel',
            new_name='recorder',
        ),
    ]
