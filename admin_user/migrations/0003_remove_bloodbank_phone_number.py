# Generated by Django 2.1.15 on 2023-04-22 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0002_clinic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloodbank',
            name='phone_number',
        ),
    ]
