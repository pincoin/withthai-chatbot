# Generated by Django 3.1 on 2020-08-16 18:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0003_auto_20200817_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='golfclub',
            name='business_hour_end',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Business hour end'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='golfclub',
            name='business_hour_start',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Business hour start'),
            preserve_default=False,
        ),
    ]