# Generated by Django 2.0.5 on 2018-06-10 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20180610_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='URL',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
