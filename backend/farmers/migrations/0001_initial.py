# Generated by Django 5.1.4 on 2025-01-07 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('size', models.FloatField()),
            ],
            options={
                'db_table': 'field',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FieldMeasurement',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('row', models.BigIntegerField()),
                ('column', models.BigIntegerField()),
            ],
            options={
                'db_table': 'field_measurement',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Seed',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('name', models.TextField(unique=True)),
                ('mass_kg', models.FloatField()),
            ],
            options={
                'db_table': 'seed',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField()),
                ('rain_mm', models.BigIntegerField()),
                ('time', models.DateTimeField()),
                ('sunny', models.BooleanField()),
            ],
            options={
                'db_table': 'weather',
                'managed': False,
            },
        ),
    ]
