import json
import random
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Machine, MachineUsage, MachineMeasurement, Employee

def get_machine_stats(request, machine_id):
    """
    Gibt die Maschinenstatistiken zurück.
    """
    measurements = MachineMeasurement.objects.filter(machine_id=machine_id).values(
        "recorded_at", "fuel_level", "engine_temperature", "oil_level", "rpm"
    )
    return JsonResponse(list(measurements), safe=False)


def get_machines(request):
    """
    Gibt eine Liste aller Maschinen zurück.
    """
    machines = Machine.objects.all().values("id", "name", "status", "category", "image_url")
    return JsonResponse(list(machines), safe=False)


def get_machine_details(request, machine_id):
    """
    Gibt die Details einer bestimmten Maschine zurück.
    """
    try:
        machine = Machine.objects.prefetch_related("assigned_employees").get(id=machine_id)
        assigned_employees = Employee.objects.filter(assigned_machines=machine)

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

        return JsonResponse(machine_data, status=200)
    except Machine.DoesNotExist:
        return JsonResponse({"error": "Maschine nicht gefunden"}, status=404)


@csrf_exempt
def add_machine(request):
    """
    Erstellt eine neue Maschine.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            serial_number = data.get("serial_number")
            year_of_manufacture = data.get("year_of_manufacture")
            status = data.get("status", "In Betrieb")
            category = data.get("category", "Traktor")
            image_url = data.get("image_url", "")

            if not name or not serial_number or not year_of_manufacture:
                return JsonResponse({"error": "Name, Seriennummer und Baujahr sind erforderlich!"}, status=400)

            try:
                year_of_manufacture = int(year_of_manufacture)
                if year_of_manufacture < 1900 or year_of_manufacture > datetime.now().year:
                    return JsonResponse({"error": "Ungültiges Baujahr!"}, status=400)
            except ValueError:
                return JsonResponse({"error": "Baujahr muss eine Zahl sein!"}, status=400)

            machine = Machine.objects.create(
                name=name,
                serial_number=serial_number,
                year_of_manufacture=year_of_manufacture,
                status=status,
                category=category,
                image_url=image_url,
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
                    "image_url": machine.image_url,
                },
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Ungültiges JSON-Format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def update_machine(request, machine_id):
    """
    Aktualisiert eine bestehende Maschine.
    """
    try:
        machine = Machine.objects.get(id=machine_id)
    except Machine.DoesNotExist:
        return JsonResponse({"error": "Maschine nicht gefunden"}, status=404)

    if request.method == "PUT":
        try:
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
                    "category": machine.category,
                },
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def delete_machine(request, machine_id):
    """
    Löscht eine Maschine anhand der ID.
    """
    try:
        machine = Machine.objects.get(id=machine_id)
        machine.delete()
        return JsonResponse({"message": "Maschine erfolgreich gelöscht"}, status=200)
    except Machine.DoesNotExist:
        return JsonResponse({"error": "Maschine nicht gefunden"}, status=404)


def get_machine_usages(request):
    """
    Gibt eine Liste aller Maschinen-Nutzungen zurück.
    """
    usages = MachineUsage.objects.all().values(
        "id", "machine__name", "employee__first_name", "employee__last_name",
        "field__name", "start_time", "end_time", "duration"
    )
    return JsonResponse(list(usages), safe=False)


@csrf_exempt
def add_machine_usage(request):
    """
    Erstellt eine neue Maschinen-Nutzung.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            usage = MachineUsage.objects.create(
                machine_id=data.get("machine_id"),
                employee_id=data.get("employee_id"),
                field_id=data.get("field_id"),
                start_time=data.get("start_time"),
            )
            return JsonResponse({"message": "Maschinen-Nutzung hinzugefügt", "usage_id": usage.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


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
    """
    Generiert zufällige Messwerte für eine bestimmte Maschine.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            machine = Machine.objects.get(id=data.get("machine_id"))

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

@csrf_exempt
def assign_machines_to_employee(request):
    """
    Weist einem Mitarbeiter eine oder mehrere Maschinen zu.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee_id = data.get("employee_id")
            machine_ids = data.get("machine_ids", [])

            employee = Employee.objects.get(id=employee_id)
            machines = Machine.objects.filter(id__in=machine_ids)

            employee.assigned_machines.set(machines)

            return JsonResponse({"message": "Maschinen erfolgreich zugewiesen"}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Mitarbeiter nicht gefunden"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Ungültige Anfrage"}, status=400)

@csrf_exempt
def assign_machines_to_employee(request):
    """
    Weist einem Mitarbeiter mehrere Maschinen zu.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee = Employee.objects.get(id=data.get("employee_id"))
            machines = Machine.objects.filter(id__in=data.get("machine_ids", []))

            employee.assigned_machines.set(machines)

            # Falls der Mitarbeiter einem Feld zugewiesen ist, setzen wir die Maschinen auch auf dieses Feld
            if employee.assigned_field:
                for machine in machines:
                    machine.assigned_field = employee.assigned_field
                    machine.save()

            return JsonResponse({"message": "Maschinen erfolgreich zugewiesen"}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({"error": "Mitarbeiter nicht gefunden"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def get_machines_by_field(request, field_id):
    """
    Gibt alle Maschinen zurück, die einem bestimmten Feld zugewiesen sind.
    """
    machines = Machine.objects.filter(assigned_field_id=field_id).values("id", "name", "category")
    
    # Maschinen-Typ hinzufügen
    machines_list = [
        {"id": machine["id"], "name": machine["name"], "type": machine["category"]}
        for machine in machines
    ]

    return JsonResponse(machines_list, safe=False)
