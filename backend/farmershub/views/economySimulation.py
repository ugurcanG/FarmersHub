import random
from datetime import datetime, timedelta

class FarmSimulation:
    def __init__(self):
        self.employees = {"Landwirt": 3, "Mechaniker": 1, "Manager": 1}
        self.machines = {"Traktor": 2, "Mähdrescher": 1, "Saatmaschine": 1}
        self.fields = [{"name": "Feld 1", "size_ha": 10, "crop": "Mais"}]
        self.market_prices = {"Mais": 0.30, "Weizen": 0.40, "Kartoffeln": 0.25}
        self.operating_hours = {"Traktor": 100, "Mähdrescher": 50}
        self.total_income = 0
        self.total_expenses = 0
        self.simulation_date = datetime(2025, 1, 1)

    def calculate_employee_costs(self):
        salaries = {"Landwirt": 2500, "Mechaniker": 3000, "Manager": 4500}
        return sum(self.employees[role] * salaries[role] for role in self.employees)

    def calculate_machine_costs(self):
        hourly_costs = {"Traktor": 10, "Mähdrescher": 15, "Saatmaschine": 12}
        return sum(self.operating_hours[machine] * hourly_costs[machine] for machine in self.machines if machine in self.operating_hours)

    def calculate_harvest(self):
        crop_yields = {"Mais": 8000, "Weizen": 6000, "Kartoffeln": 45000}
        total_yield = sum(field["size_ha"] * crop_yields[field["crop"]] for field in self.fields)
        return total_yield

    def calculate_income(self):
        total_yield = self.calculate_harvest()
        income = sum(total_yield * self.market_prices[field["crop"]] for field in self.fields)
        return income

    def simulate_month(self):
        self.simulation_date += timedelta(days=30)
        employee_costs = self.calculate_employee_costs()
        machine_costs = self.calculate_machine_costs()
        income = self.calculate_income()

        self.total_expenses += employee_costs + machine_costs
        self.total_income += income

        print(f"📅 Monat {self.simulation_date.strftime('%B %Y')}")
        print(f"👨‍🌾 Mitarbeiterkosten: {employee_costs} €")
        print(f"🚜 Maschinenkosten: {machine_costs} €")
        print(f"🌾 Einnahmen aus Ernte: {income} €")
        print(f"📈 Nettoergebnis: {income - (employee_costs + machine_costs)} €\n")

# Simulation starten
simulation = FarmSimulation()
for _ in range(12):  # 12 Monate simulieren
    simulation.simulate_month()
