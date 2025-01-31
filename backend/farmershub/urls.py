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

from .views import (
    start_field_measurement_population, get_field_health_index,
    
    # Felder
    get_fields, add_field, delete_field, update_field, get_field_details, get_field_measurements,

    # ChatGPT
    chat_with_gpt,

    # Maschinen
    get_machines, add_machine, get_machine_details, update_machine, delete_machine,

    # Mitarbeiter
    get_employees, add_employee, update_employee, delete_employee, assign_employee_to_field,

    # Maschinen-Nutzung
    get_machine_usages, add_machine_usage, generate_machine_measurements,get_machine_stats,

    # Maschinen einem Mitarbeiter zuweisen
    assign_machines_to_employee,

    # Saatgut
    get_seeds, add_seed, delete_seed
)


urlpatterns = [
    path('measurements/', start_field_measurement_population),
    path('test/', get_field_health_index),

    # Felder-URLs
    path('fields/', get_fields, name='get-fields'),
    path('fields/add/', add_field, name='add-field'),
    path('fields/delete/<int:field_id>/', delete_field, name='delete-field'),
    path('fields/update/<int:field_id>/', update_field, name='update-field'),
    path('fields/<int:field_id>/', get_field_details, name='get-field-details'),
    path('fields/<int:field_id>/measurements/', get_field_measurements, name='get-field-measurements'),

    # ChatGPT-URLs
    path('chat/', chat_with_gpt, name='chat-with-gpt'),

    # Maschinen-URLs
    path('machines/', get_machines, name='get_machines'),
    path('machines/add/', add_machine, name='add_machine'),
    path('machines/<int:machine_id>/', get_machine_details, name='get_machine_details'),
    path('machines/update/<int:machine_id>/', update_machine, name='update_machine'),
    path('machines/delete/<int:machine_id>/', delete_machine, name='delete_machine'),

    # Mitarbeiter-URLs
    path('employees/', get_employees, name='get_employees'),
    path('employees/add/', add_employee, name='add_employee'),
    path('employees/update/<int:employee_id>/', update_employee, name='update_employee'),
    path('employees/delete/<int:employee_id>/', delete_employee, name='delete_employee'),
    path('employees/assign_field/', assign_employee_to_field, name='assign_employee_to_field'),

    # Maschinen-Nutzung
    path('machine_usages/', get_machine_usages, name='get_machine_usages'),
    path('machine_usages/add/', add_machine_usage, name='add_machine_usage'),
    path('machines/generate_measurements/', generate_machine_measurements, name='generate_machine_measurements'),
    path('machines/<int:machine_id>/stats/', get_machine_stats, name='get_machine_stats'),

    # Maschinen einem Mitarbeiter zuweisen
    path('machines/assign_machines/', assign_machines_to_employee, name='assign_machines_to_employee'),

    # Saatgut-URLs
    path("seeds/", get_seeds, name="get_seeds"),
    path("seeds/add/", add_seed, name="add_seed"),
    path("seeds/delete/<int:seed_id>/", delete_seed, name="delete_seed"),
]
