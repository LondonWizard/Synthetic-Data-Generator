# hr_data.py

import os
import pandas as pd
from pydantic import BaseModel, Field
from faker import Faker
import random
import uuid
import asyncio
import logging
from chatgpt import chat_with_instructor

fake = Faker()
Faker.seed(0)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='hr_data.log')

class Employee(BaseModel):
    employee_id: str = Field(..., description="Unique identifier for the employee")
    first_name: str = Field(..., description="First name of the employee")
    last_name: str = Field(..., description="Last name of the employee")
    title: str = Field(..., description="Job title of the employee")
    department: str = Field(..., description="Department of the employee")
    salary: float = Field(..., description="Annual salary of the employee")
    hire_date: str = Field(..., description="Hire date of the employee")
    performance_review: str = Field(..., description="Annual performance review of the employee")
    payroll_data: dict = Field(..., description="Payroll data for the employee")
    employment_status: str = Field(..., description="Employment status of the employee")
    work_location: str = Field(..., description="Work location of the employee")
    benefits_enrollment: dict = Field(..., description="Benefits enrollment information")

async def generate_performance_review(first_name, last_name, title, company_data):
    prompt = f"""
You are a manager at {company_data['company_name']} preparing an annual performance review for {first_name} {last_name}, who is a {title}. Provide a realistic and professional performance review, highlighting strengths, areas for improvement, and goals for the next year. Avoid using any personal data or disallowed content.
"""
    try:
        # Use asyncio.to_thread to run the synchronous function asynchronously
        review = await asyncio.to_thread(chat_with_instructor, prompt, str)
        return review.strip() if review else "Performance review not available."
    except Exception as e:
        logging.error(f"Error generating performance review for {first_name} {last_name}: {e}")
        return "Performance review not available."

def generate_payroll_data(salary):
    # Generate payroll data similar to Gusto
    payroll = {
        'monthly_salary': round(salary / 12, 2),
        'taxes_withheld': round(salary * 0.2 / 12, 2),
        'benefits_deduction': round(salary * 0.05 / 12, 2),
        'net_pay': round((salary / 12) - (salary * 0.2 / 12) - (salary * 0.05 / 12), 2),
        'pay_period': 'Monthly',
        'last_pay_date': fake.date_between(start_date='-1m', end_date='today').isoformat()
    }
    return payroll

async def generate_employee(employee_info, company_data):
    first_name = employee_info['first_name']
    last_name = employee_info['last_name']
    title = employee_info['title']
    performance_review = await generate_performance_review(first_name, last_name, title, company_data)
    employee_info['performance_review'] = performance_review
    return employee_info

def generate_hr_data(company_data, employee_count=200, account_executive_count=50):
    employees = []
    departments = ['Sales', 'Marketing', 'Engineering', 'HR', 'Finance', 'Support']
    titles = {
        'Sales': ['Account Executive', 'Sales Manager', 'Sales Representative'],
        'Marketing': ['Marketing Manager', 'Content Strategist', 'SEO Specialist'],
        'Engineering': ['Software Engineer', 'DevOps Engineer', 'QA Engineer'],
        'HR': ['HR Manager', 'Recruiter'],
        'Finance': ['Financial Analyst', 'Accountant'],
        'Support': ['Support Specialist', 'Support Manager']
    }

    account_executive_counter = account_executive_count  # Number of Account Executives

    for _ in range(employee_count):
        department = random.choice(departments)
        title = random.choice(titles[department])

        # Ensure the number of Account Executives
        if department == 'Sales' and title == 'Account Executive':
            if account_executive_counter > 0:
                account_executive_counter -= 1
            else:
                # Choose a different title if the count is met
                title = random.choice([t for t in titles['Sales'] if t != 'Account Executive'])

        first_name = fake.first_name()
        last_name = fake.last_name()
        employee_id = f"EMP{str(uuid.uuid4())[:8]}"
        hire_date = fake.date_between(start_date='-5y', end_date='today').isoformat()
        if department == 'Sales' and title == 'Account Executive':
            salary = round(random.uniform(60000, 120000), 2)
        else:
            salary = round(random.uniform(40000, 100000), 2)
        employment_status = random.choice(['Active', 'On Leave', 'Terminated'])
        work_location = fake.city()
        benefits_enrollment = {
            'health_insurance': random.choice([True, False]),
            'dental_insurance': random.choice([True, False]),
            'retirement_plan': random.choice([True, False])
        }
        payroll_data = generate_payroll_data(salary)

        employee = {
            'employee_id': employee_id,
            'first_name': first_name,
            'last_name': last_name,
            'title': title,
            'department': department,
            'salary': salary,
            'hire_date': hire_date,
            'employment_status': employment_status,
            'work_location': work_location,
            'benefits_enrollment': benefits_enrollment,
            'payroll_data': payroll_data
        }
        employees.append(employee)

    # Generate performance reviews asynchronously
    async def main():
        tasks = [generate_employee(emp, company_data) for emp in employees]
        return await asyncio.gather(*tasks)

    # Run the event loop
    employees = asyncio.run(main())

    # Save to CSV
    df_employees = pd.DataFrame(employees)
    df_employees.to_csv(os.path.join('data', 'employees.csv'), index=False)

    logging.info("HR data generated.")
    print("HR data generated.")
    return employees