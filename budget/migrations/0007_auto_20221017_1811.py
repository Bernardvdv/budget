# Generated by Django 3.1.14 on 2022-10-17 18:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_items_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='payment_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='items',
            name='person',
            field=models.CharField(choices=[('bernard', 'Bernard'), ('tania', 'Tania')], default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='items',
            name='category',
            field=models.CharField(choices=[('home', 'Home'), ('school', 'School'), ('utility', 'Utilities'), ('food', 'Groceries'), ('mobile', 'Mobile'), ('subscription', 'Subscriptions'), ('other', 'Other')], default='Home', max_length=20),
        ),
    ]