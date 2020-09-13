# Generated by Django 3.1 on 2020-09-13 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0005_golfclub_no_order_flex_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineuser',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email address'),
        ),
        migrations.AddField(
            model_name='lineuser',
            name='lang',
            field=models.CharField(choices=[('en', 'English'), ('th', 'Thai'), ('ko', 'Korean')], default='en', max_length=16, verbose_name='Language'),
        ),
        migrations.AddField(
            model_name='lineuser',
            name='phone',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Phone number'),
        ),
    ]
