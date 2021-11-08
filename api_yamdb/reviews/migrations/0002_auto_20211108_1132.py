# Generated by Django 2.2.16 on 2021-11-08 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'user'), ('admin', 'admin'), ('moderator', 'moderator'), ('superuser', 'superuser')], max_length=20),
        ),
    ]
