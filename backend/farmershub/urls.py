"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
	path('measurements/', views.start_field_measurement_population),
	path('test/', views.get_field_health_index),

    # Felder-URLs
    path('fields/', views.get_fields, name='get-fields'),
    path('fields/add/', views.add_field, name='add-field'),
    path('fields/delete/<int:field_id>/', views.delete_field, name='delete-field'),
    path('fields/update/<int:field_id>/', views.update_field, name='update-field'),
    path('fields/<int:field_id>/', views.get_field_details, name='get-field-details'),
    path('fields/<int:field_id>/measurements/', views.get_field_measurements, name='get-field-measurements'),

    # Chatgpt-URLs
    path('chat/', views.chat_with_gpt, name='chat-with-gpt'),

    # Maschinen-URLs
    path('machines/', views.get_machines, name='get_machines'),
    path('machines/add/', views.add_machine, name='add_machine'),
    path('machines/<int:machine_id>/', views.get_machine_details, name='get_machine_details'),
    path('machines/update/<int:machine_id>/', views.update_machine, name='update_machine'),
    path('machines/delete/<int:machine_id>/', views.delete_machine, name='delete_machine'),

    # Saatgut-URLs
    path('seeds/', views.get_seeds, name='get_seeds'),
]
