# Generated by Django 4.2.5 on 2023-12-20 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_manager_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='country',
            field=models.TextField(default=''),
        ),
    ]
