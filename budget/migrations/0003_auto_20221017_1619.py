# Generated by Django 3.1.14 on 2022-10-17 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_income'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='income',
            field=models.CharField(max_length=180),
        ),
        migrations.AlterField(
            model_name='income',
            name='person',
            field=models.CharField(max_length=180),
        ),
    ]