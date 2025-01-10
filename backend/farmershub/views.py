from django.shortcuts import render
from django.http import HttpResponse
from .models import Seed

def view_helloworld(request):
    test_data = Seed.objects.all().values()
    print(test_data[0])
    
    return HttpResponse("Hello world!" + str(test_data[0]))