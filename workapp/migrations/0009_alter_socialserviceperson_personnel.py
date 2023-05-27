# Generated by Django 4.2 on 2023-05-27 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0003_alter_personnel_options'),
        ('workapp', '0008_rename_personnel_research_recorder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialserviceperson',
            name='personnel',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='PersonnelSocialServicePerson', to='baseapp.personnel'),
        ),
    ]
