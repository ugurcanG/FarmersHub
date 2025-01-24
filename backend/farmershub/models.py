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
    name = models.CharField(max_length=255, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    saat = models.ForeignKey('Seed', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'field'


class FieldMeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    row = models.BigIntegerField()
    column = models.BigIntegerField()
    temperature = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    soil_moisture = models.FloatField(blank=True, null=True)
    nutrients_level = models.FloatField(blank=True, null=True)
    health_score = models.FloatField(blank=True, null=True)
    field = models.ForeignKey(Field, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'field_measurement'


class Seed(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.TextField(unique=True)
    mass_kg = models.FloatField()
    pref_temperature = models.FloatField(blank=True, null=True)
    pref_humidity = models.FloatField(blank=True, null=True)
    pref_soil_moisture = models.FloatField(blank=True, null=True)
    pref_nutrient_level = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'seed'
