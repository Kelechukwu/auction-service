# Generated by Django 3.0.1 on 2019-12-21 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20191221_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
