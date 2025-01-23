import json

from threading import Thread

from django.core import serializers
from django.http import HttpResponse

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
    max_diff_temperature = 0.1
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
        
        for measurement in field_measurements:
            diff_temperature = measurement.temperature - seed_obj.pref_temperature
            diff_humidity = measurement.humidity - seed_obj.pref_humidity
            diff_soil_moisture = measurement.soil_moisture - seed_obj.pref_soil_moisture
            diff_nutrient_level = measurement.nutrients_level - seed_obj.pref_nutrient_level
            
            if max_diff_temperature < diff_temperature or diff_temperature < -max_diff_temperature:
                data.append(['WARNING temp', measurement.temperature, seed_obj.pref_temperature])
            if max_diff_humidity < diff_humidity or diff_humidity < -max_diff_humidity:
                data.append(['WARNING humid', measurement.humidity, seed_obj.pref_humidity])
            if max_diff_soil_moisture < diff_soil_moisture or diff_soil_moisture < -max_diff_soil_moisture:
                data.append(['WARNING moist', measurement.soil_moisture, seed_obj.pref_soil_moisture])
            if max_diff_nutrient_level < diff_nutrient_level or diff_nutrient_level < -max_diff_nutrient_level:
                data.append(['WARNING nutri', measurement.nutrients_level, seed_obj.pref_nutrient_level])
        
        data_dict = {"warnings": data}

        serialized_data = json.dumps(data_dict)
        
        return HttpResponse(serialized_data, status=200)
    except (ValueError, TypeError):
        return HttpResponse("id not valid")