# Generated by Django 4.0 on 2021-12-16 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkings',
            name='exit_time',
            field=models.DateTimeField(null=True),
        ),
    ]
