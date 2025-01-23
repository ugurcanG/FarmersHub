import random

weather_rand = random.random()
print(weather_rand)
if 0 < weather_rand < 0.1:
	print('test')
elif 0.1 < weather_rand < 0.2:
	print('test2')