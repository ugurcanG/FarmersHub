import random
import datetime
import time
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from farmershub.models import FieldMeasurement, Field # ignore error, it works on the server, dunno why


def populate_field_measurements(field: Field):
	current_datetime = datetime.datetime.now()
	
	field_size = (field.width, field.height)
	field_matrix = [[None] * field_size[0]] * field_size[1]
	
	# create field average for each measurement value:
	avg_temperature = random.triangular(-20, 60, 14)
	avg_humidity = random.triangular(0.1, 0.9, 0.4)
	avg_soil_moisture = random.triangular(70, 130, 100)
	avg_nutrient_level = random.triangular(5, 150, 80)
	
	# random events that impact measurements:
	# rain -> higher humidity, soil_moisture, slightly lower temp and nutrient level
	# dry winds -> low humidity, slightly lower soil_moisture
	weather_rand = random.random()
	if 0 < weather_rand < 0.15:
		# rain:
		avg_temperature -= 5
		avg_humidity += 0.1
		avg_soil_moisture += 20
		avg_nutrient_level -= 5
	elif 0.15 < weather_rand < 0.3:
		# dry days:
		avg_humidity -= 0.1
		avg_soil_moisture -= 20
	
	
	for i in range(len(field_matrix)):
		for j in range(len(field_matrix[i])):
			node_soil_moisture = avg_soil_moisture * (random.random() * 0.1 + 0.95)
			node_nutrient_level = avg_nutrient_level * (random.random() * 0.1 + 0.95)
			node_temperature = avg_temperature * (random.random() * 0.1 + 0.95)
			node_humidity = avg_humidity * (random.random() * 0.1 + 0.95)
			
			field_matrix[i][j] = [current_datetime, node_temperature, node_humidity, node_soil_moisture, node_nutrient_level]
			
			# send to database:
			measurement = FieldMeasurement(
				created_at=current_datetime.strftime("%Y-%m-%d %H:%M:%S+00"),
				row=i,
				column=j,
				temperature=node_temperature,
				humidity=node_humidity,
				soil_moisture=node_soil_moisture,
				nutrients_level=node_nutrient_level,
				field=field
			)
			
			measurement.save()
			
			current_datetime += datetime.timedelta(seconds=5)
			time.sleep(3)
