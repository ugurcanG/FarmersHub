export interface Field {
  id: number;
  name: string;
  width: number;
  height: number;
  size?: number; // Falls `size` direkt als Breite * Höhe berechnet wird
  saat_name: string;
  created_at?: string;
  health_score?: number | null;
}

export interface Machine {
  id: number;
  name: string;
  status: string;
  category: string;
  serial_number: string;
  year_of_manufacture: number;
  operating_hours?: number;
  image_url?: string;
  assigned_field?: Field | null;
  assigned_employees?: Employee[];
}

export interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  role: string;
  assigned_machines?: Machine[];
  assigned_field?: Field | null;
}

export interface FieldMeasurement {
  id: number;
  created_at: string;
  row: number;
  column: number;
  temperature: number;
  humidity: number;
  soil_moisture: number;
  nutrients_level: number;
  health_score: number;
  field: Field;
}

export interface MachineMeasurement {
  id: number;
  recorded_at: string;
  fuel_level?: number | null;
  engine_temperature?: number | null;
  oil_level?: number | null;
  rpm?: number | null;
  machine: Machine;
}

export interface Seed {
  id: number;
  name: string;
  mass_kg: number;
  pref_temperature?: number | null;
  pref_humidity?: number | null;
  pref_soil_moisture?: number | null;
  pref_nutrient_level?: number | null;
}

export interface ApiResponse<T> {
  data: T;
}

export interface Todo {
  id: number;
  content: string;
}

export interface Meta {
  totalCount: number;
}
