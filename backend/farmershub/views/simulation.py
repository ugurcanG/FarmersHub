import json
import random
from datetime import datetime, timedelta
from threading import Thread

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Field, FieldMeasurement, Machine, MachineMeasurement


### FELD-MESSUNGEN SIMULIEREN ###

def calculate_health_score(temperature, humidity, soil_moisture, nutrients_level, seed):
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


def populate_field_measurements(field):
    """
    Simuliert Messwerte für ein Feld basierend auf seiner Breite (columns) und Höhe (rows).
    """
    current_datetime = datetime.now()

    seed = field.saat
    if not seed:
        raise ValueError("Kein Saatgut (Seed) für dieses Feld zugeordnet.")

    # Dynamische Größe des Feldes aus der Datenbank holen
    field_width = field.width  # Spaltenanzahl
    field_height = field.height  # Reihenanzahl

    avg_temperature = random.triangular(-20, 60, 14)
    avg_humidity = random.triangular(0.1, 0.9, 0.4)
    avg_soil_moisture = random.triangular(70, 130, 100)
    avg_nutrient_level = random.triangular(5, 150, 80)

    # Wettereinfluss simulieren
    weather_rand = random.random()
    if 0 < weather_rand < 0.15:
        avg_temperature -= 5
        avg_humidity += 0.1
        avg_soil_moisture += 20
        avg_nutrient_level -= 5
    elif 0.15 < weather_rand < 0.3:
        avg_humidity -= 0.1
        avg_soil_moisture -= 20

    # Generiere Messwerte für das gesamte Feld basierend auf seiner Größe
    for row in range(field_height):  # Dynamisch: Höhe des Feldes
        for column in range(field_width):  # Dynamisch: Breite des Feldes
            temperature = avg_temperature * (random.random() * 0.1 + 0.95)
            humidity = avg_humidity * (random.random() * 0.1 + 0.95)
            soil_moisture = avg_soil_moisture * (random.random() * 0.1 + 0.95)
            nutrients_level = avg_nutrient_level * (random.random() * 0.1 + 0.95)

            # Healthscore berechnen
            health_score = calculate_health_score(temperature, humidity, soil_moisture, nutrients_level, seed)

            # Messung speichern mit dynamischen `row` und `column`
            FieldMeasurement.objects.create(
                field=field,
                row=row,  # ✅ Dynamisch aus `field.height`
                column=column,  # ✅ Dynamisch aus `field.width`
                temperature=temperature,
                humidity=humidity,
                soil_moisture=soil_moisture,
                nutrients_level=nutrients_level,
                created_at=current_datetime - timedelta(minutes=random.randint(1, 120)),
                health_score=health_score,
            )



@csrf_exempt
def generate_field_measurements(request):
    """
    API-Endpunkt zum Generieren von Messwerten für ein bestimmtes Feld.
    """
    if request.method == "POST":
        try:
            # JSON aus Request-Body laden
            data = json.loads(request.body)
            field_id = data.get("field_id")

            # Überprüfen, ob field_id existiert
            if not field_id:
                return JsonResponse({"error": "field_id fehlt in der Anfrage"}, status=400)

            # Feld abrufen
            try:
                field = Field.objects.get(id=field_id)
            except Field.DoesNotExist:
                return JsonResponse({"error": f"Feld mit ID {field_id} nicht gefunden"}, status=404)

            # Prüfen, ob das Feld ein zugewiesenes Saatgut hat
            if not field.saat:
                return JsonResponse({"error": f"Feld {field.name} hat kein zugewiesenes Saatgut"}, status=400)

            # Messwerte generieren
            populate_field_measurements(field)

            return JsonResponse({"message": f"Messwerte für Feld {field.name} generiert!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Ungültiges JSON-Format"}, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()  # Druckt den Stacktrace in die Konsole für Debugging
            return JsonResponse({"error": f"Interner Fehler: {str(e)}"}, status=500)

    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)


@csrf_exempt
def start_field_measurement_population(request):
    """
    Startet einen Thread zur Simulation von Feldmessungen.
    """
    try:
        field_id = int(request.GET.get("id"))
        field_obj = Field.objects.get(id=field_id)

        measurement_thread = Thread(target=populate_field_measurements, args=(field_obj,))
        measurement_thread.start()

        return HttpResponse("Messungssimulation gestartet", status=201)
    except (ValueError, TypeError):
        return HttpResponse("Ungültige ID", status=400)
    except Field.DoesNotExist:
        return HttpResponse("Feld nicht gefunden", status=404)


### MASCHINEN-MESSUNGEN SIMULIEREN ###

@csrf_exempt
def generate_machine_measurements(request):
    """
    API-Endpunkt zum Generieren von zufälligen Maschinenmesswerten.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            machine = Machine.objects.get(id=data.get("machine_id"))

            for _ in range(5):  # 5 zufällige Messungen erstellen
                MachineMeasurement.objects.create(
                    machine=machine,
                    recorded_at=datetime.now() - timedelta(minutes=random.randint(1, 120)),
                    fuel_level=random.uniform(10, 100),
                    engine_temperature=random.uniform(60, 120),
                    oil_level=random.uniform(20, 80),
                    rpm=random.uniform(500, 3000),
                )

            return JsonResponse({"message": f"Messwerte für Maschine {machine.name} generiert!"}, status=201)
        except Machine.DoesNotExist:
            return JsonResponse({"error": "Maschine nicht gefunden"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)
