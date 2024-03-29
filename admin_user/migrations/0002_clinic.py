# Generated by Django 2.1.15 on 2023-04-22 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('contact_person', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('website', models.URLField()),
            ],
        ),
    ]
