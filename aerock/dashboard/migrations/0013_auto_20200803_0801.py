# Generated by Django 2.2 on 2020-08-03 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_airport_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='threshold',
            old_name='threshold_value',
            new_name='threshold_value_high',
        ),
        migrations.AddField(
            model_name='threshold',
            name='threshold_value_low',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
