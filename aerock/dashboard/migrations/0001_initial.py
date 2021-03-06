# Generated by Django 2.2 on 2020-07-17 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='airport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icao_code', models.CharField(max_length=10, unique='true')),
                ('iata_code', models.CharField(max_length=10)),
                ('airport_name', models.TextField(max_length=500)),
                ('state', models.TextField(max_length=100)),
                ('city', models.TextField(max_length=100)),
                ('category', models.TextField(default='000', max_length=50)),
            ],
        ),
    ]
