from django.core import serializers
from django.http import HttpResponse
from .models import Seed

def view_helloworld(request):
    test_data = Seed.objects.all().values()
    data = Seed.objects.all()
    serialized_data = serializers.serialize('json', list(data))
    
    return HttpResponse(serialized_data)
