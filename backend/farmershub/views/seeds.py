import json
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from ..models import Seed


def get_seeds(request):
    """
    Gibt eine Liste aller verfügbaren Saatgutsorten zurück.
    """
    seeds = Seed.objects.all().values(
        "id", "name", "mass_kg", "pref_temperature", "pref_humidity",
        "pref_soil_moisture", "pref_nutrient_level", "created_at"
    )
    return JsonResponse(list(seeds), safe=False)


@csrf_exempt
def add_seed(request):
    """
    Erstellt ein neues Saatgut.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Neues Saatgut erstellen
            seed = Seed.objects.create(
                name=data.get("name"),
                mass_kg=data.get("mass_kg"),
                pref_temperature=data.get("pref_temperature"),
                pref_humidity=data.get("pref_humidity"),
                pref_soil_moisture=data.get("pref_soil_moisture"),
                pref_nutrient_level=data.get("pref_nutrient_level"),
                created_at=now(),
            )

            return JsonResponse({"message": "Saatgut hinzugefügt", "seed_id": seed.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Ungültiges JSON-Format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def delete_seed(request, seed_id):
    """
    Löscht ein Saatgut anhand der ID.
    """
    try:
        seed = Seed.objects.get(id=seed_id)
        seed.delete()
        return JsonResponse({"message": "Saatgut erfolgreich gelöscht"}, status=200)
    except Seed.DoesNotExist:
        return JsonResponse({"error": "Saatgut nicht gefunden"}, status=404)

@csrf_exempt
def update_seed(request, seed_id):
    """
    Aktualisiert eine bestehende Saatgutsorte.
    """
    try:
        seed = Seed.objects.get(id=seed_id)
    except Seed.DoesNotExist:
        return JsonResponse({"error": "Saatgut nicht gefunden"}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(seed, key, value)
            seed.save()
            return JsonResponse({"message": "Saatgut aktualisiert"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
