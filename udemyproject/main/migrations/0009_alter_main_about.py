# Generated by Django 4.2.5 on 2023-09-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_main_picname2_main_picurl2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main',
            name='about',
            field=models.TextField(default=''),
        ),
    ]
