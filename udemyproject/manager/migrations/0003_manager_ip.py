# Generated by Django 4.2.5 on 2023-12-20 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_manager_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='ip',
            field=models.CharField(default='0.0.0.0', max_length=20),
        ),
    ]
