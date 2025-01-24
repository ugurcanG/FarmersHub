import json

from threading import Thread
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse


from . import simulation
from .models import Seed, Field, FieldMeasurement


# http://127.0.0.1:8000/helloworld/
def view_helloworld(request):
    test_data = Seed.objects.all().values()
    data = Seed.objects.all()
    serialized_data = serializers.serialize('json', list(data))
    
    return HttpResponse(serialized_data)


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
        # Felder mit den relevanten Daten abrufen
        fields = Field.objects.all().values(
            'id', 'name', 'created_at', 'width', 'height', 'saat__name'
        )  # 'saat__name' für den Namen des Saatguts
        for field in fields:
            field['size'] = field['width'] * field['height']  # Fläche berechnen
        return JsonResponse(list(fields), safe=False)
    
    except (ValueError, TypeError):
        return HttpResponse("id not valid")
    
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
                from .models import Seed
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