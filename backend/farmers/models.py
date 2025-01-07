# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Field(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    size = models.FloatField()
    saat = models.ForeignKey('Seed', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'field'


class FieldMeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    row = models.BigIntegerField()
    column = models.BigIntegerField()
    field = models.ForeignKey(Field, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'field_measurement'


class Seed(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.TextField(unique=True)
    mass_kg = models.FloatField()

    class Meta:
        managed = False
        db_table = 'seed'


class Weather(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    rain_mm = models.BigIntegerField()
    time = models.DateTimeField()
    sunny = models.BooleanField()
    field = models.ForeignKey(Field, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'weather'
