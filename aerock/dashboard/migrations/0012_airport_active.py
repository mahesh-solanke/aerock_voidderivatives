# Generated by Django 2.2 on 2020-07-30 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20200729_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='airport',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]