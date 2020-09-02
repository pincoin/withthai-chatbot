# Generated by Django 3.1 on 2020-09-02 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0003_auto_20200902_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='golfbookingpromotion',
            name='discount_method',
            field=models.IntegerField(choices=[(0, 'Percent'), (1, 'Minus'), (2, 'Assign')], db_index=True, default=0, verbose_name='Discount method'),
        ),
    ]
