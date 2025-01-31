# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# ---------------------------------
# Feld-Modell
# ---------------------------------
class Field(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    saat = models.ForeignKey('Seed', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'field'

# ---------------------------------
# Feldmessungen-Modell
# ---------------------------------
class FieldMeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    row = models.BigIntegerField()
    column = models.BigIntegerField()
    temperature = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    soil_moisture = models.FloatField(blank=True, null=True)
    nutrients_level = models.FloatField(blank=True, null=True)
    health_score = models.FloatField(blank=True, null=True)
    field = models.ForeignKey('Field', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'field_measurement'

# ---------------------------------
# Saatgut-Modell
# ---------------------------------
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

# ---------------------------------
# Mitarbeiter-Modell
# ---------------------------------
class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=[
        ('Landwirt', 'Landwirt'),
        ('Mechaniker', 'Mechaniker'),
        ('Manager', 'Manager'),
    ], default='Landwirt')
    assigned_machines = models.ManyToManyField('Machine', blank=True)
    assigned_field = models.ForeignKey('Field', on_delete=models.SET_NULL, blank=True, null=True)  # NEU: Feldzuweisung
    last_activity = models.DateTimeField(auto_now=True)  # NEU: Letzte Aktivität
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

# ---------------------------------
# Maschinen-Modell
# ---------------------------------
class Machine(models.Model):
    MACHINE_CATEGORIES = [
        ('Traktor', 'Traktor'),
        ('Mähdrescher', 'Mähdrescher'),
        ('Anhänger', 'Anhänger'),
        ('Zubehör', 'Zubehör'),
        ('Saatmaschine', 'Saatmaschine'),
    ]

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=[
        ('In Betrieb', 'In Betrieb'),
        ('Wartung erforderlich', 'Wartung erforderlich'),
        ('Defekt', 'Defekt'),
    ], default='In Betrieb')
    category = models.CharField(max_length=50, choices=MACHINE_CATEGORIES, default='Traktor')
    image_url = models.URLField(blank=True, null=True)
    year_of_manufacture = models.IntegerField(blank=True, null=True)  # Neues Feld
    operating_hours = models.FloatField(default=0.0)  # Betriebsstunden
    serial_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    assigned_employees = models.ManyToManyField('Employee', blank=True)
    assigned_field = models.ForeignKey('Field', models.SET_NULL, blank=True, null=True)  # Welches Feld wird gerade bearbeitet?
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'machine'

    def __str__(self):
        return f"{self.name} ({self.category})"

# ---------------------------------
# Maschinen-Nutzungshistorie
# ---------------------------------
class MachineUsage(models.Model):
    id = models.BigAutoField(primary_key=True)
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True)
    field = models.ForeignKey('Field', on_delete=models.SET_NULL, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)  # Berechnete Dauer in Stunden

    class Meta:
        db_table = 'machine_usage'

    def __str__(self):
        return f"{self.machine.name} genutzt von {self.employee} auf {self.field} ({self.start_time})"

# ---------------------------------
# Maschinen-Wartung
# ---------------------------------
class MachineMaintenance(models.Model):
    id = models.BigAutoField(primary_key=True)
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    maintenance_date = models.DateTimeField()
    next_maintenance = models.DateTimeField(blank=True, null=True)
    description = models.TextField()

    class Meta:
        db_table = 'machine_maintenance'

    def __str__(self):
        return f"Wartung an {self.machine.name} am {self.maintenance_date}"

# ---------------------------------
# Maschinen-Messwerte
# ---------------------------------
class MachineMeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    recorded_at = models.DateTimeField(auto_now_add=True)
    fuel_level = models.FloatField(blank=True, null=True)
    engine_temperature = models.FloatField(blank=True, null=True)
    oil_level = models.FloatField(blank=True, null=True)
    rpm = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'machine_measurement'

    def __str__(self):
        return f"Messwert für {self.machine.name} ({self.recorded_at})"
