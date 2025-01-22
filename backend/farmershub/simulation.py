import random
import datetime
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from farmershub.models import FieldMeasurement, Field # DO NOT CHANGE! IT IS NEEDED!!!! (yes i hate it too)


# Anforderungen:
# messschritte DONE
# abhängigkeit in zeit und raum DONE
# besondere events
# in echtzeit an die datenbank

soil_moisture = None # 15-50%
nutrient_level = None # 5-150ppm
temperature = None # -20 - 60 degrees celcius
humidity = None # 10-70% relative air humidity
current_datetime = datetime.datetime.now()

field_size = (random.randint(1, 5), random.randint(1, 5))
field = [[None] * field_size[0]] * field_size[1]

# create field average for each measurement value:
avg_soil_moisture = random.random() * 0.35 + 0.15
avg_nutrient_level = random.random() * 145 + 5
avg_temperature = random.random() * 60 - 20
avg_humidity = random.random() * 0.6 + 0.1

# random events that impact measurements:
# rain -> higher humidity, soil_moisture, slightly lower temp and nutrient level
# dry winds -> low humidity, slightly lower soil_moisture

for i in range(len(field)):
	for j in range(len(field[i])):
		node_soil_moisture = avg_soil_moisture * (random.random() * 0.1 + 0.95)
		node_nutrient_level = avg_nutrient_level * (random.random() * 0.1 + 0.95)
		node_temperature = avg_temperature * (random.random() * 0.1 + 0.95)
		node_humidity = avg_humidity * (random.random() * 0.1 + 0.95)
		
		field[i][j] = [current_datetime, node_temperature, node_humidity, node_soil_moisture, node_nutrient_level]
		
		# send to database:
		measurement = FieldMeasurement(
			created_at=current_datetime.strftime("%Y-%m-%d %H:%M:%S+00"),
			row=i,
			column=j,
			temperature=node_temperature,
			humidity=node_humidity,
			soil_moisture=node_soil_moisture,
			nutrients_level=node_nutrient_level,
			field=Field.objects.first()
		)
		
		measurement.save()

		# increment datetime by time between measurements
		# for realtime simulation wait here a few secs
		current_datetime += datetime.timedelta(seconds=5)
