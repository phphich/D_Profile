# Generated by Django 4.2 on 2023-05-22 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='baseapp.division')),
                ('personnel', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='baseapp.personnel')),
            ],
        ),
    ]