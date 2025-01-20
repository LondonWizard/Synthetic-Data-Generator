import os
import random
import json
import argparse
from datetime import date, timedelta
from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()

# ----------------------------------------------------------
# 1. Pydantic Models for Performance Records
# ----------------------------------------------------------
class NursePerformanceRecord(BaseModel):
    employee_id: str
    name: str
    role: str
    record_date: str
    patient_satisfaction_score: float = Field(..., description="Patient satisfaction percentage")
    readmission_rate: float = Field(..., description="Percentage readmission rate")
    compliance_score: float = Field(..., description="Compliance logs score, e.g. hand hygiene, documentation")
    charting_timeliness: float = Field(..., description="Percentage of charts completed within 24h window")

class PhysicianPerformanceRecord(BaseModel):
    employee_id: str
    name: str
    role: str
    record_date: str
    complication_rate: float = Field(..., description="Complications as a % of total cases")
    readmission_rate: float = Field(..., description="Readmission %")
    follow_up_adherence: float = Field(..., description="Percentage of patients with recommended follow-up visits")
    patient_outcomes_score: float = Field(..., description="General measure of patient outcomes (0-100)")

class PharmacistPerformanceRecord(BaseModel):
    employee_id: str
    name: str
    role: str
    record_date: str
    prescription_volume: int = Field(..., description="Number of prescriptions filled in a period")
    error_rate: float = Field(..., description="Percentage of prescription errors")
    patient_counseling_score: float = Field(..., description="Score reflecting quality of counseling")
    avg_wait_time_minutes: float = Field(..., description="Average wait time in minutes")

# ----------------------------------------------------------
# 2. Generate dates in last quarter of 2024
# ----------------------------------------------------------
def generate_dates_in_last_quarter_of_2024():
    start_date = date(2024, 10, 1)
    end_date = date(2024, 12, 31)
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)

# ----------------------------------------------------------
# 3. Generate employees for the three roles
# ----------------------------------------------------------
def generate_employees(n_nurses, n_physicians, n_pharmacists):
    """
    Creates employees for each role with random names.
    """
    employees = []
    employee_index = 1

    # Nurses
    for _ in range(n_nurses):
        employees.append({
            "employee_id": f"EID{employee_index:03d}",
            "name": fake.name(),
            "role": "Nurse"
        })
        employee_index += 1

    # Physicians
    for _ in range(n_physicians):
        employees.append({
            "employee_id": f"EID{employee_index:03d}",
            "name": fake.name(),
            "role": "Physician"
        })
        employee_index += 1

    # Pharmacists
    for _ in range(n_pharmacists):
        employees.append({
            "employee_id": f"EID{employee_index:03d}",
            "name": fake.name(),
            "role": "Pharmacist"
        })
        employee_index += 1

    return employees

# ----------------------------------------------------------
# 4. Generate performance data for each role
# ----------------------------------------------------------
def generate_nurse_performance_data(employees):
    records = []
    for emp in employees:
        if emp["role"].lower() == "nurse":
            for single_date in generate_dates_in_last_quarter_of_2024():
                record = NursePerformanceRecord(
                    employee_id=emp["employee_id"],
                    name=emp["name"],
                    role=emp["role"],
                    record_date=str(single_date),
                    patient_satisfaction_score=round(random.uniform(70, 100), 2),
                    readmission_rate=round(random.uniform(0, 5), 2),
                    compliance_score=round(random.uniform(80, 100), 2),
                    charting_timeliness=round(random.uniform(70, 100), 2),
                )
                records.append(record)
    return records

def generate_physician_performance_data(employees):
    records = []
    for emp in employees:
        if emp["role"].lower() == "physician":
            for single_date in generate_dates_in_last_quarter_of_2024():
                record = PhysicianPerformanceRecord(
                    employee_id=emp["employee_id"],
                    name=emp["name"],
                    role=emp["role"],
                    record_date=str(single_date),
                    complication_rate=round(random.uniform(0, 10), 2),
                    readmission_rate=round(random.uniform(0, 8), 2),
                    follow_up_adherence=round(random.uniform(70, 100), 2),
                    patient_outcomes_score=round(random.uniform(50, 100), 2),
                )
                records.append(record)
    return records

def generate_pharmacist_performance_data(employees):
    records = []
    for emp in employees:
        if emp["role"].lower() == "pharmacist":
            for single_date in generate_dates_in_last_quarter_of_2024():
                record = PharmacistPerformanceRecord(
                    employee_id=emp["employee_id"],
                    name=emp["name"],
                    role=emp["role"],
                    record_date=str(single_date),
                    prescription_volume=random.randint(50, 200),
                    error_rate=round(random.uniform(0, 5), 2),
                    patient_counseling_score=round(random.uniform(60, 100), 2),
                    avg_wait_time_minutes=round(random.uniform(2, 20), 2),
                )
                records.append(record)
    return records

# ----------------------------------------------------------
# 5. Save data as JSON in an LLM-friendly format
# ----------------------------------------------------------
def save_records_to_json(records, role_name, output_filename):
    """
    Saves the given records (list of Pydantic objects) to a JSON file with 
    a structure that includes dataset_name, description, fields, data array.
    """
    out_dir = "healthcaredata"
    os.makedirs(out_dir, exist_ok=True)

    if not records:
        # Create an empty JSON file if no records
        empty_data = {
            "dataset_name": f"{role_name.capitalize()} Performance (Q4 2024)",
            "description": f"Daily performance metrics for {role_name}s from Oct 1 to Dec 31, 2024",
            "fields": [],
            "data": []
        }
        with open(os.path.join(out_dir, output_filename), "w") as f:
            json.dump(empty_data, f, indent=2)
        return
    

    # Decide how to fill out the fields array
    # Each Pydantic model has descriptions for each field; we can retrieve them:
    # For convenience, let's just do a small manual mapping:
    fields_info = []
    if role_name.lower() == "nurse":
        fields_info = [
            {"name": "employee_id", "description": "Unique employee code"},
            {"name": "name", "description": "Employee's full name"},
            {"name": "role", "description": "Job role (Nurse)"},
            {"name": "record_date", "description": "Date of record (YYYY-MM-DD)"},
            {"name": "patient_satisfaction_score", "description": "Patient satisfaction (%)"},
            {"name": "readmission_rate", "description": "Readmission (%)"},
            {"name": "compliance_score", "description": "Compliance logs (%)"},
            {"name": "charting_timeliness", "description": "Chart completion timeliness (%)"}
        ]
    elif role_name.lower() == "physician":
        fields_info = [
            {"name": "employee_id", "description": "Unique employee code"},
            {"name": "name", "description": "Employee's full name"},
            {"name": "role", "description": "Job role (Physician)"},
            {"name": "record_date", "description": "Date of record (YYYY-MM-DD)"},
            {"name": "complication_rate", "description": "Complications (%)"},
            {"name": "readmission_rate", "description": "Readmission (%)"},
            {"name": "follow_up_adherence", "description": "Follow-up adherence (%)"},
            {"name": "patient_outcomes_score", "description": "Overall patient outcomes (0-100)"}
        ]
    elif role_name.lower() == "pharmacist":
        fields_info = [
            {"name": "employee_id", "description": "Unique employee code"},
            {"name": "name", "description": "Employee's full name"},
            {"name": "role", "description": "Job role (Pharmacist)"},
            {"name": "record_date", "description": "Date of record (YYYY-MM-DD)"},
            {"name": "prescription_volume", "description": "Number of prescriptions filled"},
            {"name": "error_rate", "description": "Prescription errors (%)"},
            {"name": "patient_counseling_score", "description": "Counseling quality score (0-100)"},
            {"name": "avg_wait_time_minutes", "description": "Average wait time for patients (minutes)"}
        ]
    else:
        fields_info = []

    # Convert the Pydantic records to dicts
    data_rows = [r.dict() for r in records]

    # Build the final JSON structure
    output_data = {
        "dataset_name": f"{role_name.capitalize()} Performance (Q4 2024)",
        "description": f"Daily performance metrics for {role_name}s from Oct 1 to Dec 31, 2024",
        "fields": fields_info,
        "data": data_rows
    }

    # Write to JSON
    with open(os.path.join(out_dir, output_filename), "w") as f:
        json.dump(output_data, f, indent=2)

# ----------------------------------------------------------
# 6. Main
# ----------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic healthcare performance data for Nurses, Physicians, and Pharmacists, in JSON format."
    )
    parser.add_argument("--nurses", type=int, default=5, help="Number of nurse employees")
    parser.add_argument("--physicians", type=int, default=4, help="Number of physician employees")
    parser.add_argument("--pharmacists", type=int, default=3, help="Number of pharmacist employees")

    args = parser.parse_args()

    # 1) Create the employees
    employees = generate_employees(
        n_nurses=args.nurses,
        n_physicians=args.physicians,
        n_pharmacists=args.pharmacists
    )

    # 2) Generate performance data
    nurse_records = generate_nurse_performance_data(employees)
    physician_records = generate_physician_performance_data(employees)
    pharmacist_records = generate_pharmacist_performance_data(employees)

    # 3) Save each to its own JSON file in a friendly format
    save_records_to_json(nurse_records,      "nurse",      "nurse_performance.json")
    save_records_to_json(physician_records,  "physician",  "physician_performance.json")
    save_records_to_json(pharmacist_records, "pharmacist", "pharmacist_performance.json")

    print("Synthetic healthcare performance data generated in JSON format!")
    print("Check the 'healthcaredata/' folder for .json files.")


if __name__ == "__main__":
    main()