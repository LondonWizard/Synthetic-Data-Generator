# sales_data.py

import os
import pandas as pd
from pydantic import BaseModel, Field
from faker import Faker
import utils
import random

fake = Faker()
Faker.seed(0)

class SalesTarget(BaseModel):
    team_member_id: str = Field(..., description="ID of the sales team member")
    employee_id: str = Field(..., description="Employee ID")
    name: str = Field(..., description="Name of the team member")
    role: str = Field(..., description="Role (AE or BDR)")
    total_target: float = Field(..., description="Total sales target for 2024")
    new_clients_target: float = Field(..., description="Target for new clients")
    existing_clients_target: float = Field(..., description="Target for existing clients")

def generate_sales_data(company_data, employees):
    total_new_revenue = 6_000_000
    new_clients_revenue = 4_500_000
    existing_clients_revenue = 1_500_000

    # Sales Team
    sales_team = []
    num_aes = 8
    num_bdrs = 4

    # Filter employees in Sales department
    sales_employees = [e for e in employees if e['department'] == 'Sales' and e['title'] not in ['VP of Sales']]

    # Generate Account Executives
    aes = random.sample(sales_employees, num_aes)
    for ae in aes:
        sales_target = SalesTarget(
            team_member_id=ae['employee_id'],
            employee_id=ae['employee_id'],
            name=f"{ae['first_name']} {ae['last_name']}",
            role="Account Executive",
            total_target=(6_000_000 / num_aes),
            new_clients_target=(4_500_000 / num_aes),
            existing_clients_target=(1_500_000 / num_aes)
        )
        sales_team.append(sales_target.dict())

    # Remove AEs from sales_employees
    sales_employees = [e for e in sales_employees if e not in aes]

    # Generate BDRs
    bdrs = random.sample(sales_employees, num_bdrs)
    for bdr in bdrs:
        sales_target = SalesTarget(
            team_member_id=bdr['employee_id'],
            employee_id=bdr['employee_id'],
            name=f"{bdr['first_name']} {bdr['last_name']}",
            role="BDR",
            total_target=((6_000_000 / num_aes) * 0.5),
            new_clients_target=((4_500_000 / num_aes) * 0.5),
            existing_clients_target=((1_500_000 / num_aes) * 0.5)
        )
        sales_team.append(sales_target.dict())

    # Save to CSV
    df = pd.DataFrame(sales_team)
    df.to_csv(os.path.join('data', 'sales_targets.csv'), index=False)

    # Generate Customers
    customers = []
    for i in range(1, 101):
        customer = {
            'customer_id': f"CUST{str(i).zfill(4)}",
            'company_name': fake.company(),
            'product_tier': fake.random_element(elements=('Basic', 'Standard', 'Premium')),
            'purchase_date': fake.date_between(start_date='-1y', end_date='today').isoformat(),
            'renewal_date': fake.date_between(start_date='+1y', end_date='+2y').isoformat(),
            'account_manager_id': random.choice(aes)['employee_id']
        }
        customers.append(customer)

    df_customers = pd.DataFrame(customers)
    df_customers.to_csv(os.path.join('data', 'customers.csv'), index=False)

    # Update shared data
    utils.sales_team = sales_team
    utils.customers = customers

    print("Sales data generated.")
    return customers, sales_team