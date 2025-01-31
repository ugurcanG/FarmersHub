import json
import logging
import random
from datetime import datetime, timedelta
from threading import Thread

from django.conf import settings
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from openai import OpenAI

from . import simulation
from .models import (
    Seed, Field, FieldMeasurement, Machine, MachineUsage, 
    Employee, MachineMeasurement
)

logger = logging.getLogger(__name__)



# Saatgutliste abrufen
def get_seeds(request):
    seeds = Seed.objects.all().values("id", "name", "mass_kg", "pref_temperature", "pref_humidity", "pref_soil_moisture", "pref_nutrient_level", "created_at")
    return JsonResponse(list(seeds), safe=False)

# Neues Saatgut hinzufügen
@csrf_exempt
def add_seed(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            seed = Seed.objects.create(
                name=data.get("name"),
                mass_kg=data.get("mass_kg"),
                pref_temperature=data.get("pref_temperature"),
                pref_humidity=data.get("pref_humidity"),
                pref_soil_moisture=data.get("pref_soil_moisture"),
                pref_nutrient_level=data.get("pref_nutrient_level"),
                created_at=now()
            )
            return JsonResponse({"message": "Saatgut hinzugefügt", "seed_id": seed.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# Saatgut löschen
@csrf_exempt
def delete_seed(request, seed_id):
    try:
        seed = Seed.objects.get(id=seed_id)
        seed.delete()
        return JsonResponse({"message": "Saatgut erfolgreich gelöscht"}, status=200)
    except Seed.DoesNotExist:
        return JsonResponse({"error": "Saatgut nicht gefunden"}, status=404)

# http://127.0.0.1:8000/measurements/?id=2
def start_field_measurement_population(request):
    try:
        field_id = int(request.GET.get('id'))
        field_obj = Field.objects.get(id=field_id)

        measurement_thread = Thread(target=simulation.populate_field_measurements, args=(field_obj,))
        measurement_thread.start()

        return HttpResponse("process started", status=201)
    except (ValueError, TypeError):
        return HttpResponse("id not valid")


def get_field_health_index(request):
    max_diff_temperature = 15
    max_diff_humidity = 15
    max_diff_soil_moisture = 10
    max_diff_nutrient_level = 50

    try:
        field_id = int(request.GET.get('id'))
        field_obj = Field.objects.get(id=field_id)
        field_size = field_obj.width * field_obj.height

        field_measurements = FieldMeasurement.objects.all().order_by('-id')[:field_size]
        seed_obj = Seed.objects.get(id=field_obj.saat_id)

        data = []
        health_score = float(field_size * 4)

        for measurement in field_measurements:
            diff_temperature = measurement.temperature - seed_obj.pref_temperature
            diff_humidity = measurement.humidity - seed_obj.pref_humidity
            diff_soil_moisture = measurement.soil_moisture - seed_obj.pref_soil_moisture
            diff_nutrient_level = measurement.nutrients_level - seed_obj.pref_nutrient_level

            if max_diff_temperature < diff_temperature or diff_temperature < -max_diff_temperature:
                data.append(['WARNING temperature', measurement.temperature, seed_obj.pref_temperature])
                health_score -= 1
            if max_diff_humidity < diff_humidity or diff_humidity < -max_diff_humidity:
                data.append(['WARNING humidity', measurement.humidity, seed_obj.pref_humidity])
                health_score -= 1
            if max_diff_soil_moisture < diff_soil_moisture or diff_soil_moisture < -max_diff_soil_moisture:
                data.append(['WARNING soil_moisture', measurement.soil_moisture, seed_obj.pref_soil_moisture])
                health_score -= 1
            if max_diff_nutrient_level < diff_nutrient_level or diff_nutrient_level < -max_diff_nutrient_level:
                data.append(['WARNING nutrients_level', measurement.nutrients_level, seed_obj.pref_nutrient_level])
                health_score -= 1

        data_dict = {
            "field_size": field_size,
            "health_score": f"{health_score}/{field_size * 4}",
            "warnings": data,
        }

        serialized_data = json.dumps(data_dict)

        return HttpResponse(serialized_data, status=200)
    except (ValueError, TypeError):
        return HttpResponse("id not valid")

# http://127.0.0.1:8000/fields/
def get_fields(request):
    try:
        # Abrufen aller Felder
        fields = Field.objects.all()

        field_list = []
        for field in fields:
            # Berechne die Feldgröße
            size = field.width * field.height

            # Finde die zugehörigen Messungen
            field_measurements = FieldMeasurement.objects.filter(field=field)

            # Berechne den durchschnittlichen Healthscore
            if field_measurements.exists():
                total_health_score = field_measurements.aggregate(models.Sum('health_score'))['health_score__sum'] or 0
                measurement_count = field_measurements.count()
                avg_health_score = total_health_score / measurement_count if measurement_count > 0 else None
            else:
                avg_health_score = None

            # Daten für das Feld vorbereiten
            field_data = {
                "id": field.id,
                "name": field.name,
                "width": field.width,
                "height": field.height,
                "size": size,
                "saat__name": field.saat.name if field.saat else None,
                "created_at": field.created_at,
                "health_score": avg_health_score,  # Durchschnittlicher Healthscore
            }

            field_list.append(field_data)

        return JsonResponse(field_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# http://127.0.0.1:8000/fields/add/
@csrf_exempt
def add_field(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))

        # Hole die Werte aus dem Request
        name = data.get("name")
        width = data.get("width")
        height = data.get("height")
        saat_name = data.get("saat_name")

        if not width or not height:
            return JsonResponse({"error": "Breite und Höhe sind erforderlich!"}, status=400)

        try:
            width = int(width)  # Konvertiere zu Integer
            height = int(height)  # Konvertiere zu Integer
        except ValueError:
            return JsonResponse({"error": "Breite und Höhe müssen Zahlen sein!"}, status=400)

        # Saatgut suchen, falls angegeben
        seed = Seed.objects.filter(name=saat_name).first() if saat_name else None

        # Feld erstellen
        field = Field.objects.create(name=name, width=width, height=height, saat=seed)

        # Antwortdaten vorbereiten
        field_data = {
            "id": field.id,
            "name": field.name,
            "width": field.width,
            "height": field.height,
            "size": field.width * field.height,
            "saat__name": field.saat.name if field.saat else None,
            "created_at": field.created_at,
        }
        return JsonResponse(field_data, status=201)

# http://127.0.0.1:8000/fields/delete/<int:field_id>/
@csrf_exempt
def delete_field(request, field_id):
    if request.method == "DELETE":
        try:
            # Hole das Feld mit der gegebenen ID
            field = Field.objects.get(id=field_id)
            field.delete()  # Lösche das Feld
            return JsonResponse({"message": "Feld erfolgreich gelöscht"}, status=200)
        except Field.DoesNotExist:
            return JsonResponse({"error": "Feld nicht gefunden"}, status=404)
    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)


# http://127.0.0.1:8000/fields/update/<int:field_id>/
@csrf_exempt
def update_field(request, field_id):
    if request.method == "PUT":
        try:
            # Hole das Feld, das aktualisiert werden soll
            field = Field.objects.get(id=field_id)
        except Field.DoesNotExist:
            return JsonResponse({"error": "Feld nicht gefunden"}, status=404)

        # Parse die JSON-Daten aus dem Request
        try:
            data = json.loads(request.body)
            name = data.get("name")
            width = data.get("width")
            height = data.get("height")
            saat_name = data.get("saat_name")

            if name is not None:
                field.name = name
            if width is not None:
                field.width = int(width)
            if height is not None:
                field.height = int(height)

            # Aktualisiere Saatgut, falls angegeben
            if saat_name is not None:
                seed = Seed.objects.filter(name=saat_name).first()
                field.saat = seed

            field.save()

            # Berechne die Größe des Feldes
            field_data = {
                "id": field.id,
                "name": field.name,
                "width": field.width,
                "height": field.height,
                "size": field.width * field.height,
                "saat__name": field.saat.name if field.saat else None,
                "created_at": field.created_at,
            }
            return JsonResponse(field_data, status=200)
        except ValueError:
            return JsonResponse({"error": "Ungültige Daten"}, status=400)
    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)


def get_field_details(request, field_id):
    try:
        field = Field.objects.get(id=field_id)
        data = {
            "id": field.id,
            "name": field.name,
            "size": field.width * field.height,
            "created_at": field.created_at,
            "saat__name": field.saat.name if field.saat else None,
            "health_score": FieldMeasurement.objects.filter(field=field).aggregate(models.Avg('health_score'))['health_score__avg'] or 0
        }
        return JsonResponse(data, safe=False)
    except Field.DoesNotExist:
        return JsonResponse({"error": "Feld nicht gefunden"}, status=404)

def get_field_measurements(request, field_id):
    try:
        # Hole alle Messwerte für das gegebene Feld
        measurements = FieldMeasurement.objects.filter(field_id=field_id).order_by('created_at')

        # Konvertiere die Daten in eine Liste von Dictionaries
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




client = OpenAI(api_key=settings.OPENAI_API_KEY)

# http://127.0.0.1:8000/chat/
@csrf_exempt
def chat_with_gpt(request):
    if request.method == "POST":
        try:
            # Anfrage-Daten parsen
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                logger.error("Nachricht fehlt")
                return JsonResponse({"error": "Nachricht fehlt"}, status=400)

            # Anfrage an OpenAI senden
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Bitte antworte immer auf Deutsch."},
                    {"role": "user", "content": user_message}
                ]
            )

            # Antwort extrahieren
            gpt_reply = response.choices[0].message.content
            return JsonResponse({"reply": gpt_reply}, status=200)

        except Exception as e:
            logger.exception("Fehler in der Funktion chat_with_gpt:")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)



def get_machines(request):
    machines = Machine.objects.all().values('id', 'name', 'status', 'category', 'image_url')
    return JsonResponse(list(machines), safe=False)

def get_machine_details(request, machine_id):
    try:
        machine = Machine.objects.prefetch_related("assigned_employees").get(id=machine_id)  # 🚀 WICHTIG

        # Lade die Mitarbeiter
        assigned_employees = Employee.objects.filter(assigned_machines=machine)  # Stelle sicher, dass es eine Liste ist

        machine_data = {
            "id": machine.id,
            "name": machine.name,
            "status": machine.status,
            "category": machine.category,
            "serial_number": machine.serial_number,
            "year_of_manufacture": machine.year_of_manufacture,
            "operating_hours": machine.operating_hours,
            "image_url": machine.image_url,
            "assigned_field": {
                "id": machine.assigned_field.id,
                "name": machine.assigned_field.name
            } if machine.assigned_field else None,
            "assigned_employees": [
                {"id": emp.id, "first_name": emp.first_name, "last_name": emp.last_name}
                for emp in assigned_employees
            ],
        }

        print("🚀 Backend sendet:", machine_data)  # Debugging

        return JsonResponse(machine_data, status=200)
    except Machine.DoesNotExist:
        return JsonResponse({"error": "Maschine nicht gefunden"}, status=404)

# Neue Maschine hinzufügen
@csrf_exempt
def add_machine(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            print("Empfangene Daten:", data)  # Debugging-Log für empfangene JSON-Daten

            name = data.get("name")
            serial_number = data.get("serial_number")
            year_of_manufacture = data.get("year_of_manufacture")
            status = data.get("status", "In Betrieb")
            category = data.get("category", "Traktor")
            image_url = data.get("image_url", "")

            # Validierung
            if not name:
                return JsonResponse({"error": "Maschinenname ist erforderlich!"}, status=400)
            if not serial_number:
                return JsonResponse({"error": "Seriennummer ist erforderlich!"}, status=400)
            if not year_of_manufacture:
                return JsonResponse({"error": "Baujahr ist erforderlich!"}, status=400)

            # Stelle sicher, dass `year_of_manufacture` eine Zahl ist
            try:
                year_of_manufacture = int(year_of_manufacture)
            except ValueError:
                return JsonResponse({"error": "Baujahr muss eine Zahl sein!"}, status=400)

            if year_of_manufacture < 1900 or year_of_manufacture > datetime.now().year:
                return JsonResponse({"error": "Ungültiges Baujahr!"}, status=400)

            # Maschine erstellen
            machine = Machine.objects.create(
                name=name,
                serial_number=serial_number,
                year_of_manufacture=year_of_manufacture,
                status=status,
                category=category,
                image_url=image_url
            )

            return JsonResponse({
                "message": "Maschine hinzugefügt",
                "machine": {
                    "id": machine.id,
                    "name": machine.name,
                    "serial_number": machine.serial_number,
                    "year_of_manufacture": machine.year_of_manufacture,
                    "status": machine.status,
                    "category": machine.category,
                    "image_url": machine.image_url
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Ungültiges JSON-Format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Eine Maschine aktualisieren
@csrf_exempt
def update_machine(request, machine_id):
    try:
        machine = Machine.objects.get(id=machine_id)
    except Machine.DoesNotExist:
        return JsonResponse({"error": "Maschine nicht gefunden"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        machine.name = data.get("name", machine.name)
        machine.status = data.get("status", machine.status)
        machine.category = data.get("category", machine.category)
        machine.save()
        return JsonResponse({
            "message": "Maschine aktualisiert",
            "machine": {
                "id": machine.id,
                "name": machine.name,
                "status": machine.status,
                "category": machine.category
            }
        }, status=200)

# Eine Maschine löschen
@csrf_exempt
def delete_machine(request, machine_id):
    try:
        machine = Machine.objects.get(id=machine_id)
        machine.delete()
        return JsonResponse({"message": "Maschine erfolgreich gelöscht"}, status=200)
    except Machine.DoesNotExist:
        return JsonResponse({"error": "Maschine nicht gefunden"}, status=404)
    

# Maschinen-Nutzungen abrufen
def get_machine_usages(request):
    usages = MachineUsage.objects.all().values(
        'id', 'machine__name', 'employee__first_name', 'employee__last_name', 'field__name', 'start_time', 'end_time', 'duration'
    )
    return JsonResponse(list(usages), safe=False)

# Maschinen-Messwerte abrufen
def get_machine_stats(request, machine_id):
    measurements = MachineMeasurement.objects.filter(machine_id=machine_id).values(
        "recorded_at", "fuel_level", "engine_temperature", "oil_level", "rpm"
    )
    return JsonResponse(list(measurements), safe=False)

# Neue Maschinen-Nutzung hinzufügen
@csrf_exempt
def add_machine_usage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        machine_id = data.get("machine_id")
        employee_id = data.get("employee_id")
        field_id = data.get("field_id")
        start_time = data.get("start_time")

        usage = MachineUsage.objects.create(
            machine_id=machine_id,
            employee_id=employee_id,
            field_id=field_id,
            start_time=start_time
        )
        return JsonResponse({"message": "Maschinen-Nutzung hinzugefügt", "usage_id": usage.id}, status=201)
    

def get_employees(request):
    employees = Employee.objects.all()
    employees_list = []

    for employee in employees:
        assigned_machines = employee.assigned_machines.all()
        employees_list.append({
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "role": employee.role,
            "assigned_field": {
                "id": employee.assigned_field.id,
                "name": employee.assigned_field.name
            } if employee.assigned_field else None,
            "assigned_machines": [
                {"id": machine.id, "name": machine.name} for machine in assigned_machines
            ]
        })

    return JsonResponse(employees_list, safe=False)

# Neuen Mitarbeiter hinzufügen
@csrf_exempt
def add_employee(request):
    if request.method == "POST":
        data = json.loads(request.body)
        employee = Employee.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            role=data.get("role", "Landwirt"),
        )
        return JsonResponse({
            "message": "Mitarbeiter hinzugefügt",
            "employee": {
                "id": employee.id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "role": employee.role
            }
        }, status=201)

# Mitarbeiter aktualisieren
@csrf_exempt
def update_employee(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Mitarbeiter nicht gefunden"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        employee.first_name = data.get("first_name", employee.first_name)
        employee.last_name = data.get("last_name", employee.last_name)
        employee.role = data.get("role", employee.role)
        employee.save()

        return JsonResponse({
            "message": "Mitarbeiter aktualisiert",
            "employee": {
                "id": employee.id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "role": employee.role
            }
        }, status=200)

# Mitarbeiter löschen
@csrf_exempt
def delete_employee(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        return JsonResponse({"message": "Mitarbeiter erfolgreich gelöscht"}, status=200)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Mitarbeiter nicht gefunden"}, status=404)




@csrf_exempt
def assign_machines_to_employee(request):
    if request.method == "POST":
        data = json.loads(request.body)
        employee_id = data.get("employee_id")
        machine_ids = data.get("machine_ids", [])

        try:
            employee = Employee.objects.get(id=employee_id)
            machines = Machine.objects.filter(id__in=machine_ids)

            # Maschinen dem Mitarbeiter zuweisen
            employee.assigned_machines.set(machines)

            # Falls Mitarbeiter einem Feld zugewiesen ist, setzen wir die Maschinen auch auf dieses Feld
            if employee.assigned_field:
                for machine in machines:
                    machine.assigned_field = employee.assigned_field
                    machine.save()

            return JsonResponse({"message": "Maschinen erfolgreich zugewiesen"}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Mitarbeiter nicht gefunden"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)

@csrf_exempt
def generate_field_measurements(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            field_id = data.get("field_id")

            field = Field.objects.get(id=field_id)
            simulation.populate_field_measurements(field)  # Simulationsfunktion aufrufen

            return JsonResponse({"message": f"Messwerte für Feld {field.name} generiert!"}, status=201)
        except Field.DoesNotExist:
            return JsonResponse({"error": "Feld nicht gefunden"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)

def get_machine_measurements(request, machine_id):
    """
    Gibt alle Messwerte für eine bestimmte Maschine zurück.
    """
    try:
        measurements = MachineMeasurement.objects.filter(machine_id=machine_id).values(
            "id", "recorded_at", "fuel_level", "engine_temperature", "oil_level", "rpm"
        )
        return JsonResponse(list(measurements), safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def generate_machine_measurements(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            machine_id = data.get("machine_id")

            machine = Machine.objects.get(id=machine_id)

            # Simulierte Messwerte für die Maschine generieren
            for _ in range(5):
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


@csrf_exempt
def assign_employee_to_field(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee_id = data.get("employee_id")
            field_id = data.get("field_id")

            employee = Employee.objects.get(id=employee_id)
            field = Field.objects.get(id=field_id)

            # Mitarbeiter einem Feld zuweisen
            employee.assigned_field = field
            employee.save()

            # Falls der Mitarbeiter Maschinen hat, setzen wir diese auf dasselbe Feld
            for machine in employee.assigned_machines.all():
                machine.assigned_field = field
                machine.save()

            return JsonResponse({"message": "Mitarbeiter erfolgreich zugewiesen"}, status=200)
        except (Employee.DoesNotExist, Field.DoesNotExist):
            return JsonResponse({"error": "Mitarbeiter oder Feld nicht gefunden"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)