# Generated by Django 5.1.5 on 2025-06-15 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile_photo',
            new_name='profile_pic',
        ),
    ]
