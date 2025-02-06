from django.http import JsonResponse
from ..models import Seed, Field, Employee, Machine
import random

def get_market_data(request):
    """Generiert aktuelle Marktpreise und wirtschaftliche Simulation."""
    
    # Dynamische Marktpreise für Saatgut & Ernte
    seed_prices = {seed.name: round(random.uniform(1.5, 5.0), 2) for seed in Seed.objects.all()}
    harvest_prices = {seed.name: round(random.uniform(50, 200), 2) for seed in Seed.objects.all()}
    
    # Kosten
    field_costs = Field.objects.count() * 500  # Pro Feld 500€ Wartungskosten
    employee_costs = Employee.objects.count() * 2500  # Pro Mitarbeiter 2500€ Lohnkosten
    machine_maintenance = Machine.objects.count() * 1000  # Wartungskosten pro Maschine

    # Einnahmen durch Ernte
    total_revenue = sum(harvest_prices[seed.name] * seed.mass_kg for seed in Seed.objects.all())

    # Gesamtgewinn/-verlust
    total_expenses = field_costs + employee_costs + machine_maintenance
    profit_loss = total_revenue - total_expenses

    return JsonResponse({
        "seed_prices": seed_prices,
        "harvest_prices": harvest_prices,
        "expenses": {
            "fields": field_costs,
            "employees": employee_costs,
            "machines": machine_maintenance
        },
        "total_revenue": total_revenue,
        "profit_loss": profit_loss
    })
