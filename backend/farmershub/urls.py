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

    # Mitarbeiter-URLs
    path('employees/', views.get_employees, name='get_employees'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/update/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('employees/assign_field/', views.assign_employee_to_field, name='assign_employee_to_field'),


    # Maschinen-Nutzung
    path('machine_usages/', views.get_machine_usages, name='get_machine_usages'),
    path('machine_usages/add/', views.add_machine_usage, name='add_machine_usage'),
    path('machines/generate_measurements/', views.generate_machine_measurements, name='generate_machine_measurements'),

    # Maschinen einem Mitarbeiter zuweisen
    path('machines/assign_machines/', views.assign_machines_to_employee, name='assign_machines_to_employee'),

    # Saatgut-URLs
    path('seeds/', views.get_seeds, name='get_seeds'),
]
