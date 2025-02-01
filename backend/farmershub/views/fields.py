import json
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from threading import Thread

from . import simulation
from ..models import Field, FieldMeasurement, Seed


def get_fields(request):
    """
    Gibt eine Liste aller Felder zurück.
    """
    try:
        fields = Field.objects.all()
        field_list = [
            {
                "id": field.id,
                "name": field.name,
                "width": field.width,
                "height": field.height,
                "size": field.width * field.height,
                "saat__name": field.saat.name if field.saat else None,
                "created_at": field.created_at,
                "health_score": FieldMeasurement.objects.filter(field=field)
                    .aggregate(models.Avg("health_score"))["health_score__avg"] or 0,
            }
            for field in fields
        ]
        return JsonResponse(field_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def add_field(request):
    """
    Erstellt ein neues Feld.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            seed = Seed.objects.filter(name=data.get("saat_name")).first()
            field = Field.objects.create(
                name=data.get("name"),
                width=int(data.get("width")),
                height=int(data.get("height")),
                saat=seed
            )
            return JsonResponse({
                "id": field.id,
                "name": field.name,
                "width": field.width,
                "height": field.height,
                "size": field.width * field.height,
                "saat__name": field.saat.name if field.saat else None,
                "created_at": field.created_at,
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def update_field(request, field_id):
    """
    Aktualisiert ein bestehendes Feld.
    """
    if request.method == "PUT":
        try:
            field = Field.objects.get(id=field_id)
        except Field.DoesNotExist:
            return JsonResponse({"error": "Feld nicht gefunden"}, status=404)

        try:
            data = json.loads(request.body)
            field.name = data.get("name", field.name)
            field.width = int(data.get("width", field.width))
            field.height = int(data.get("height", field.height))
            if "saat_name" in data:
                field.saat = Seed.objects.filter(name=data["saat_name"]).first()

            field.save()

            return JsonResponse({
                "id": field.id,
                "name": field.name,
                "width": field.width,
                "height": field.height,
                "size": field.width * field.height,
                "saat__name": field.saat.name if field.saat else None,
                "created_at": field.created_at,
            }, status=200)
        except ValueError:
            return JsonResponse({"error": "Ungültige Daten"}, status=400)


@csrf_exempt
def delete_field(request, field_id):
    """
    Löscht ein Feld anhand der ID.
    """
    try:
        Field.objects.get(id=field_id).delete()
        return JsonResponse({"message": "Feld erfolgreich gelöscht"}, status=200)
    except Field.DoesNotExist:
        return JsonResponse({"error": "Feld nicht gefunden"}, status=404)


def get_field_details(request, field_id):
    """
    Gibt die Details eines bestimmten Feldes zurück.
    """
    try:
        field = Field.objects.get(id=field_id)
        data = {
            "id": field.id,
            "name": field.name,
            "size": field.width * field.height,
            "created_at": field.created_at,
            "saat__name": field.saat.name if field.saat else None,
            "health_score": FieldMeasurement.objects.filter(field=field)
                .aggregate(models.Avg('health_score'))['health_score__avg'] or 0
        }
        return JsonResponse(data, safe=False)
    except Field.DoesNotExist:
        return JsonResponse({"error": "Feld nicht gefunden"}, status=404)


def get_field_measurements(request, field_id):
    """
    Gibt alle Messwerte eines bestimmten Feldes zurück.
    """
    try:
        measurements = FieldMeasurement.objects.filter(field_id=field_id).order_by("created_at")
        measurement_list = [
            {
                "id": measurement.id,
                "created_at": measurement.created_at,
                "temperature": measurement.temperature,
                "humidity": measurement.humidity,
                "soil_moisture": measurement.soil_moisture,
                "nutrients_level": measurement.nutrients_level,
                "health_score": measurement.health_score,
            }
            for measurement in measurements
        ]
        return JsonResponse(measurement_list, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def start_field_measurement_population(request):
    """
    Startet eine Simulation zur Messwerterfassung für ein bestimmtes Feld.
    """
    try:
        field_id = int(request.GET.get("id"))
        field_obj = Field.objects.get(id=field_id)

        measurement_thread = Thread(target=simulation.populate_field_measurements, args=(field_obj,))
        measurement_thread.start()

        return HttpResponse("process started", status=201)
    except (ValueError, TypeError):
        return HttpResponse("id not valid")


def get_field_health_index(request):
    """
    Berechnet den Gesundheitsindex eines Feldes anhand der letzten Messwerte.
    """
    MAX_DIFF_TEMPERATURE = 15
    MAX_DIFF_HUMIDITY = 15
    MAX_DIFF_SOIL_MOISTURE = 10
    MAX_DIFF_NUTRIENT_LEVEL = 50

    try:
        field_id = int(request.GET.get("id"))
        field_obj = Field.objects.get(id=field_id)
        field_size = field_obj.width * field_obj.height

        field_measurements = FieldMeasurement.objects.filter(field=field_obj).order_by("-id")[:field_size]
        seed_obj = Seed.objects.get(id=field_obj.saat_id)

        data = []
        health_score = float(field_size * 4)

        for measurement in field_measurements:
            diff_temperature = measurement.temperature - seed_obj.pref_temperature
            diff_humidity = measurement.humidity - seed_obj.pref_humidity
            diff_soil_moisture = measurement.soil_moisture - seed_obj.pref_soil_moisture
            diff_nutrient_level = measurement.nutrients_level - seed_obj.pref_nutrient_level

            if abs(diff_temperature) > MAX_DIFF_TEMPERATURE:
                data.append(["WARNING temperature", measurement.temperature, seed_obj.pref_temperature])
                health_score -= 1
            if abs(diff_humidity) > MAX_DIFF_HUMIDITY:
                data.append(["WARNING humidity", measurement.humidity, seed_obj.pref_humidity])
                health_score -= 1
            if abs(diff_soil_moisture) > MAX_DIFF_SOIL_MOISTURE:
                data.append(["WARNING soil_moisture", measurement.soil_moisture, seed_obj.pref_soil_moisture])
                health_score -= 1
            if abs(diff_nutrient_level) > MAX_DIFF_NUTRIENT_LEVEL:
                data.append(["WARNING nutrients_level", measurement.nutrients_level, seed_obj.pref_nutrient_level])
                health_score -= 1

        return JsonResponse({
            "field_size": field_size,
            "health_score": f"{health_score}/{field_size * 4}",
            "warnings": data,
        }, status=200)
    except (ValueError, TypeError):
        return HttpResponse("id not valid")
