# Generated by Django 4.0.4 on 2022-04-11 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="user",
            name="role",
        ),
        migrations.RemoveField(
            model_name="user",
            name="user_permissions",
        ),
        migrations.DeleteModel(
            name="Role",
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
