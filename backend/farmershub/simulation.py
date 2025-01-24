import random
import datetime
import time
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from farmershub.models import FieldMeasurement, Field # ignore error, it works on the server, dunno why


def calculate_health_score(
    temperature, humidity, soil_moisture, nutrients_level, seed
):
    """
    Berechnet den Healthscore basierend auf den Differenzen zu den optimalen Werten.
    """
    max_diff_temperature = 15
    max_diff_humidity = 0.3
    max_diff_soil_moisture = 20
    max_diff_nutrient_level = 50

    health_score = 4  # Startwert für einen perfekten Score

    if abs(temperature - seed.pref_temperature) > max_diff_temperature:
        health_score -= 1
    if abs(humidity - seed.pref_humidity) > max_diff_humidity:
        health_score -= 1
    if abs(soil_moisture - seed.pref_soil_moisture) > max_diff_soil_moisture:
        health_score -= 1
    if abs(nutrients_level - seed.pref_nutrient_level) > max_diff_nutrient_level:
        health_score -= 1

    return max(0, health_score)  # Score kann nicht negativ sein


def populate_field_measurements(field: Field):
    """
    Erstellt Messdaten für ein Feld und berechnet den Healthscore.
    """
    current_datetime = datetime.datetime.now()

    # Feldgröße berechnen
    field_size = (field.width, field.height)

    # Seed-Referenz abrufen
    seed = field.saat

    if not seed:
        raise ValueError("Kein Saatgut (Seed) für dieses Feld zugeordnet.")

    avg_temperature = random.triangular(-20, 60, 14)
    avg_humidity = random.triangular(0.1, 0.9, 0.4)
    avg_soil_moisture = random.triangular(70, 130, 100)
    avg_nutrient_level = random.triangular(5, 150, 80)

    # Wettereinfluss auf Messungen simulieren
    weather_rand = random.random()
    if 0 < weather_rand < 0.15:
        avg_temperature -= 5
        avg_humidity += 0.1
        avg_soil_moisture += 20
        avg_nutrient_level -= 5
    elif 0.15 < weather_rand < 0.3:
        avg_humidity -= 0.1
        avg_soil_moisture -= 20

    # Messungen generieren
    for i in range(field_size[1]):  # Zeilen
        for j in range(field_size[0]):  # Spalten
            temperature = avg_temperature * (random.random() * 0.1 + 0.95)
            humidity = avg_humidity * (random.random() * 0.1 + 0.95)
            soil_moisture = avg_soil_moisture * (random.random() * 0.1 + 0.95)
            nutrients_level = avg_nutrient_level * (random.random() * 0.1 + 0.95)

            # Healthscore berechnen
            health_score = calculate_health_score(
                temperature, humidity, soil_moisture, nutrients_level, seed
            )

            # Messung speichern
            measurement = FieldMeasurement(
                created_at=current_datetime,
                row=i,
                column=j,
                temperature=temperature,
                humidity=humidity,
                soil_moisture=soil_moisture,
                nutrients_level=nutrients_level,
                health_score=health_score,  # Berechneter Healthscore
                field=field,
            )
            measurement.save()

            current_datetime += datetime.timedelta(seconds=5)