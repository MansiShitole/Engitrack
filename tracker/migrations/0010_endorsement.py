# Generated by Django 5.1.5 on 2025-06-19 04:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_achievement'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Endorsement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endorsed_at', models.DateTimeField(auto_now_add=True)),
                ('endorsed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endorsements', to='tracker.skill')),
            ],
            options={
                'unique_together': {('skill', 'endorsed_by')},
            },
        ),
    ]
