# Generated by Django 3.1 on 2020-09-13 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0007_lineuser_membership_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineuser',
            name='membership_id',
        ),
        migrations.AddField(
            model_name='lineusermembership',
            name='membership_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Membership ID'),
        ),
    ]
