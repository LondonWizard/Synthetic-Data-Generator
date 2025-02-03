#!/usr/bin/env python3

"""
Generate synthetic healthcare data for a specified number of Pharmacists, Physicians, and Nurses.
Each employee gets their own folder under "healthcaredata/<EMP_ID>", and in that folder, one .txt file 
per day from Dec 2 - Dec 6, 2024 (JSON-formatted).

Some data fields are randomly omitted to simulate "missing data."

Usage:
  python generate_healthcare_data.py --pharmacists 2 --physicians 3 --nurses 4
"""

import os
import json
import argparse
import random
import logging
from datetime import date, timedelta
from faker import Faker

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]  # prints to console
)

fake = Faker()

# -----------------------------
# 1. Constants and Date Range
# -----------------------------
START_DATE = date(2024, 12, 2)
END_DATE = date(2024, 12, 6)

# Helper to yield daily dates in range
def date_range(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

# -----------------------------
# 2. Generate Employees
# -----------------------------
def generate_employees(n_pharmacists, n_physicians, n_nurses):
    """
    Create a list of employees with minimal HR data, 
    each with a role, ID, name, etc.
    """
    employees = []
    roles = {
        "Pharmacist": n_pharmacists,
        "Physician": n_physicians,
        "Nurse": n_nurses
    }

    employee_index = 1
    for role, count in roles.items():
        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            employee_id = f"EMP-{employee_index:04d}"
            employee_index += 1

            # Basic HR info
            employee_info = {
                "employee_id": employee_id,
                "first_name": first_name,
                "last_name": last_name,
                "name": f"{first_name} {last_name}",
                "role": role,
                "hire_date": str(fake.date_between(start_date='-5y', end_date='-1y')),
                "work_location": fake.city() + ", " + fake.state_abbr(),
                "remote": random.choice([True, False]),
                "department": f"{role} Department"
            }
            employees.append(employee_info)

    return employees

# -------------------------------------
# 3. Generate Synthetic Daily Data
# -------------------------------------
def generate_daily_data(employee, date_obj, missing_data_probability=0.1):
    """
    Generate JSON for:
      - basic HR info
      - daily healthcare metrics tailored by role
      - random but logically consistent values
      - randomly omit some fields to simulate missing data
    """
    # Common or universal metrics for any healthcare worker
    operational_efficiency = {
        "avg_patient_wait_time_minutes": round(random.uniform(5, 60), 2),
        "num_patient_appointments": random.randint(5, 20),
        "cost_to_collect": round(random.uniform(200, 2000), 2)
    }

    compliance_risk_management = {
        "policy_compliance_rate": round(random.uniform(85, 100), 2),
        "legal_compliance_status": random.choice(["Compliant", "Non-Compliant"]),
        "audit_violations": random.randint(0, 2),
        "frequency_of_incidents": random.randint(0, 3),
        "avg_resolution_time_days": round(random.uniform(0.5, 3.0), 2),
        "staff_training_completion_rate": round(random.uniform(70, 100), 2),
        "record_keeping_accuracy_rate": round(random.uniform(80, 100), 2),
        "timeliness_of_doc_updates_days": round(random.uniform(0.1, 1.5), 2)
    }

    risk_mitigation_metrics = {
        "identified_hazards": random.randint(0, 5),
        "vulnerability_assessment_score": round(random.uniform(0, 10), 2),
        "likelihood_of_risk_occurrence_percent": round(random.uniform(5, 30), 2),
        "impact_assessment": random.choice(["Severe", "Moderate", "Minor"]),
        "preventive_actions_implemented": random.randint(0, 3),
        "effectiveness_of_detective_controls_percent": round(random.uniform(50, 100), 2),
        "incident_tracking_frequency": random.randint(0, 2),
        "contingency_plan_exists": random.choice(["Yes", "No"]),
        "recovery_time_objective_hours": random.randint(12, 72)
    }

    role = employee["role"].lower()
    if role == "physician":
        patient_outcomes = {
            "infection_rate_per_1000": round(random.uniform(0, 3), 2),
            "readmission_rate_percent": round(random.uniform(5, 15), 2),
            "mortality_rate_per_1000": round(random.uniform(0, 2), 2),
            "patient_satisfaction_score": round(random.uniform(70, 100), 2)
        }
        financial_performance = {
            "avg_claim_processing_days": round(random.uniform(5, 20), 2),
            "days_in_accounts_receivable": random.randint(30, 90),
            "net_collection_rate_percent": round(random.uniform(80, 99), 2)
        }
    elif role == "nurse":
        patient_outcomes = {
            "infection_rate_per_1000": round(random.uniform(0, 2), 2),
            "readmission_rate_percent": round(random.uniform(4, 12), 2),
            "mortality_rate_per_1000": round(random.uniform(0, 1), 2),
            "patient_satisfaction_score": round(random.uniform(75, 100), 2)
        }
        financial_performance = {
            "avg_claim_processing_days": round(random.uniform(3, 15), 2),
            "days_in_accounts_receivable": random.randint(20, 60),
            "net_collection_rate_percent": round(random.uniform(85, 98), 2)
        }
    elif role == "pharmacist":
        patient_outcomes = {
            "infection_rate_per_1000": round(random.uniform(0, 1), 2),
            "readmission_rate_percent": round(random.uniform(2, 8), 2),
            "mortality_rate_per_1000": 0.0,
            "patient_satisfaction_score": round(random.uniform(65, 100), 2)
        }
        financial_performance = {
            "avg_claim_processing_days": round(random.uniform(1, 10), 2),
            "days_in_accounts_receivable": random.randint(15, 45),
            "net_collection_rate_percent": round(random.uniform(80, 99), 2)
        }
    else:
        patient_outcomes = {
            "infection_rate_per_1000": 0,
            "readmission_rate_percent": 0,
            "mortality_rate_per_1000": 0,
            "patient_satisfaction_score": 0
        }
        financial_performance = {
            "avg_claim_processing_days": 0,
            "days_in_accounts_receivable": 0,
            "net_collection_rate_percent": 0
        }

    data_for_day = {
        "employee_info": {
            "employee_id": employee["employee_id"],
            "name": employee["name"],
            "role": employee["role"],
            "department": employee["department"],
            "hire_date": employee["hire_date"],
            "work_location": employee["work_location"],
            "remote": employee["remote"]
        },
        "date": str(date_obj),
        "patient_outcomes": patient_outcomes,
        "operational_efficiency": operational_efficiency,
        "financial_performance": financial_performance,
        "compliance_risk_management": compliance_risk_management,
        "risk_mitigation_metrics": risk_mitigation_metrics
    }

    # 3a. Possibly remove some fields to simulate missing data
    #     We'll randomly choose a few top-level keys or sub-keys to remove.
    #     For example, ~10% chance that "operational_efficiency" is missing entirely, 
    #     or that "patient_satisfaction_score" is missing, etc.

    if random.random() < missing_data_probability:
        # randomly remove entire sections or subfields
        keys_to_consider = [
            "patient_outcomes", 
            "operational_efficiency", 
            "financial_performance", 
            "compliance_risk_management", 
            "risk_mitigation_metrics"
        ]
        # pick 1 random key from the above to remove
        to_remove = random.choice(keys_to_consider)
        data_for_day.pop(to_remove, None)

    # 3b. Also remove random subfields in some cases
    for section in ["patient_outcomes", "operational_efficiency", "financial_performance"]:
        if section in data_for_day and random.random() < missing_data_probability:
            subdict = data_for_day[section]
            if subdict:  # remove a random subkey
                random_key = random.choice(list(subdict.keys()))
                subdict.pop(random_key, None)

    return data_for_day

# -----------------------------------------
# 4. Main routine to generate the files
# -----------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic healthcare data for Pharmacists, Physicians, and Nurses."
    )
    parser.add_argument("--pharmacists", type=int, default=1, help="Number of Pharmacists")
    parser.add_argument("--physicians", type=int, default=1, help="Number of Physicians")
    parser.add_argument("--nurses", type=int, default=1, help="Number of Nurses")

    args = parser.parse_args()

    # 1) Generate the employees
    employees = generate_employees(
        n_pharmacists=args.pharmacists,
        n_physicians=args.physicians,
        n_nurses=args.nurses
    )
    logging.info(f"Generated {len(employees)} employees.")

    # 2) Use absolute path for the output folder to avoid path issues
    output_root = os.path.abspath("healthcaredata")
    logging.info(f"Absolute path for output folder: {output_root}")

    try:
        os.makedirs(output_root, exist_ok=True)
        logging.info(f"Created/Verified root folder: {output_root}")
    except Exception as e:
        logging.error(f"Failed to create folder '{output_root}': {e}")
        return

    # 3) For each employee, create a subfolder under healthcaredata/<EMP_ID>
    for emp in employees:
        # Make subfolder name safe for OS
        safe_emp_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in emp["employee_id"])
        emp_folder = os.path.join(output_root, safe_emp_id)

        try:
            os.makedirs(emp_folder, exist_ok=True)
            logging.info(f"Creating subfolder for employee '{emp['employee_id']}' -> {emp_folder}")
        except Exception as e:
            logging.error(f"Failed to create subfolder '{emp_folder}': {e}")
            continue

        # 4) Generate daily JSON data for each day (Dec 2 - Dec 6).
        for day in date_range(START_DATE, END_DATE):
            daily_data = generate_daily_data(emp, day, missing_data_probability=0.1)
            file_path = os.path.join(emp_folder, f"{day}.txt")

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(daily_data, f, indent=2)
            except Exception as e:
                logging.error(f"Failed to write file '{file_path}': {e}")

    logging.info("Synthetic healthcare data generation complete!")
    print("Synthetic healthcare data generated!")
    print(f"Check the '{output_root}/' folder for employee subfolders and daily .txt files.")


if __name__ == "__main__":
    main()
