# Generated by Django 3.1.14 on 2023-06-30 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_auto_20230630_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='name',
            field=models.CharField(max_length=180),
        ),
    ]
