# Generated by Django 5.1.3 on 2024-12-04 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0002_alter_habit_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="habit",
            name="dt",
        ),
        migrations.AddField(
            model_name="habit",
            name="tm",
            field=models.TimeField(blank=True, null=True, verbose_name="время"),
        ),
    ]