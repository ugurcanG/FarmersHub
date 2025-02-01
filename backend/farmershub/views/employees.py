import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Employee, Field


def get_employees(request):
    """
    Gibt eine Liste aller Mitarbeiter zurück.
    """
    employees = Employee.objects.all()
    employees_list = [
        {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "role": employee.role,
            "assigned_field": {
                "id": employee.assigned_field.id,
                "name": employee.assigned_field.name
            } if employee.assigned_field else None,
            "assigned_machines": [
                {"id": machine.id, "name": machine.name} for machine in employee.assigned_machines.all()
            ],
        }
        for employee in employees
    ]

    return JsonResponse(employees_list, safe=False)


@csrf_exempt
def add_employee(request):
    """
    Erstellt einen neuen Mitarbeiter.
    """
    if request.method == "POST":
        try:
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
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def update_employee(request, employee_id):
    """
    Aktualisiert einen bestehenden Mitarbeiter.
    """
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Mitarbeiter nicht gefunden"}, status=404)

    if request.method == "PUT":
        try:
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
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def delete_employee(request, employee_id):
    """
    Löscht einen Mitarbeiter anhand der ID.
    """
    try:
        Employee.objects.get(id=employee_id).delete()
        return JsonResponse({"message": "Mitarbeiter erfolgreich gelöscht"}, status=200)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Mitarbeiter nicht gefunden"}, status=404)

@csrf_exempt
def assign_employee_to_field(request):
    """
    Weist einem Mitarbeiter ein Feld zu.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee = Employee.objects.get(id=data.get("employee_id"))
            field = Field.objects.get(id=data.get("field_id"))

            # Mitarbeiter zuweisen
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

def get_employees_by_field(request, field_id):
    """
    Gibt alle Mitarbeiter zurück, die einem bestimmten Feld zugewiesen sind.
    """
    employees = Employee.objects.filter(assigned_field_id=field_id).values("id", "first_name", "last_name", "role")

    # Den vollständigen Namen in einem Feld zusammenfassen
    employees_list = [
        {
            "id": emp["id"],
            "name": f"{emp['first_name']} {emp['last_name']}",
            "role": emp["role"],
        }
        for emp in employees
    ]

    return JsonResponse(employees_list, safe=False)
