# Generated by Django 3.1 on 2020-09-13 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0006_auto_20200913_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineuser',
            name='membership_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Membership ID'),
        ),
    ]
