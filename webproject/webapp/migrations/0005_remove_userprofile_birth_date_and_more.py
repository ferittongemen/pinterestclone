# Generated by Django 4.2.7 on 2023-11-28 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_rename_user_userprofile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='location',
        ),
    ]