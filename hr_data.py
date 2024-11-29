# hr_data.py

import os
import pandas as pd
from pydantic import BaseModel, Field
from faker import Faker
import utils
from chatgpt import chat_with_instructor

fake = Faker()
Faker.seed(0)

# Define the Pydantic model for an Employee
class Employee(BaseModel):
    employee_id: str = Field(..., description="Unique identifier for the employee")
    first_name: str = Field(..., description="First name of the employee")
    last_name: str = Field(..., description="Last name of the employee")
    email: str = Field(..., description="Email address of the employee")
    hire_date: str = Field(..., description="Hiring date of the employee")
    title: str = Field(..., description="Job title of the employee")
    department: str = Field(..., description="Department of the employee")
    location: str = Field(..., description="Work location of the employee")
    remote: bool = Field(..., description="Whether the employee is remote or in-person")

# Define the Pydantic model for a Resume
class Resume(BaseModel):
    applicant_id: str = Field(..., description="Unique identifier for the applicant")
    name: str = Field(..., description="Name of the applicant")
    email: str = Field(..., description="Email of the applicant")
    position_applied: str = Field(..., description="Position the applicant applied for")
    resume_text: str = Field(..., description="Text content of the resume")

def generate_hr_data(company_data):
    num_employees = 40
    employees = []

    # Predefined lists of SaaS-specific job titles
    saas_job_titles = {
        'Executive': ['CEO', 'CTO', 'CFO', 'COO', 'CIO'],
        'Sales': ['VP of Sales', 'Sales Manager', 'Account Executive', 'Sales Development Representative'],
        'Support': ['VP of Support', 'Customer Support Manager', 'Support Specialist', 'Technical Support Engineer'],
        'HR': ['VP of People', 'HR Manager', 'Recruiting Manager', 'HR Coordinator'],
        'Marketing': ['VP of Marketing', 'Marketing Manager', 'Content Strategist', 'SEO Specialist'],
        'Finance': ['Finance Manager', 'Accountant', 'Financial Analyst', 'Controller'],
        'R&D': ['Lead Developer', 'Software Engineer', 'Product Manager', 'QA Engineer'],
        'Admin': ['Office Manager', 'Administrative Assistant']
    }

    departments = list(saas_job_titles.keys())

    # Define key positions
    key_positions = [
        {'title': 'CEO', 'department': 'Executive'},
        {'title': 'VP of Sales', 'department': 'Sales'},
        {'title': 'VP of Support', 'department': 'Support'},
        {'title': 'VP of People', 'department': 'HR'},
        {'title': 'VP of Marketing', 'department': 'Marketing'},
        {'title': 'Finance Manager', 'department': 'Finance'},
        {'title': 'Recruiting Manager', 'department': 'HR'}
    ]

    employee_id = 1

    # Generate key positions
    for position in key_positions:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@{company_data['company_name'].lower().replace(' ', '')}.com"
        employee = Employee(
            employee_id=f"EMP{str(employee_id).zfill(4)}",
            first_name=first_name,
            last_name=last_name,
            email=email,
            hire_date=fake.date_between(start_date='-4y', end_date='today').isoformat(),
            title=position['title'],
            department=position['department'],
            location=fake.city(),
            remote=fake.boolean(chance_of_getting_true=30)
        )
        employees.append(employee.dict())
        employee_id += 1

    # Generate other employees
    for _ in range(num_employees - len(key_positions)):
        department = fake.random_element(elements=departments)
        title = fake.random_element(elements=saas_job_titles[department])

        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@{company_data['company_name'].lower().replace(' ', '')}.com"
        employee = Employee(
            employee_id=f"EMP{str(employee_id).zfill(4)}",
            first_name=first_name,
            last_name=last_name,
            email=email,
            hire_date=fake.date_between(start_date='-4y', end_date='today').isoformat(),
            title=title,
            department=department,
            location=fake.city(),
            remote=fake.boolean(chance_of_getting_true=30)
        )
        employees.append(employee.dict())
        employee_id += 1

    # Save to CSV
    df = pd.DataFrame(employees)
    df.to_csv(os.path.join('data', 'employees.csv'), index=False)

    # Update shared data
    utils.employees = employees

    print("HR data generated.")

    # Generate Resumes
    generate_resumes(company_data)

    return employees

def generate_resumes(company_data):
    resumes = []
    for i in range(1, 101):
        prompt = f"""
        Generate a realistic resume for a job applicant applying to {company_data['company_name']}. Include:
        - A name
        - An email address
        - A position they are applying for (common in a SaaS company)
        - A professional summary
        - Work experience relevant to the position
        - Education
        Provide this information in JSON format matching the following schema:

        {{
            "applicant_id": "string",
            "name": "string",
            "email": "string",
            "position_applied": "string",
            "resume_text": "string"
        }}
        """
        # Use chat_with_instructor to generate the resume
        resume_data = chat_with_instructor(prompt, response_model=Resume)
        resume_dict = resume_data.dict()
        resume_dict['applicant_id'] = f"APP{str(i).zfill(4)}"
        resumes.append(resume_dict)

    # Save to CSV
    df_resumes = pd.DataFrame(resumes)
    df_resumes.to_csv(os.path.join('data', 'resumes.csv'), index=False)

    print("Resumes generated.")