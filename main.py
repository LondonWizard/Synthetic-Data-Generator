# main.py

import os
from company_info import generate_company_info
from hr_data import generate_hr_data
from sales_data import generate_sales_data
from crm_data import generate_crm_data
from support_data import generate_support_data
from finance_data import generate_finance_data
from marketing_data import generate_marketing_data

def main():
    # Create the data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Generate Company Info
    company_data = generate_company_info()

    # Generate HR data
    employees = generate_hr_data(company_data)

    # Generate Sales data
    customers, sales_team = generate_sales_data(company_data, employees)

    # Generate CRM data
    generate_crm_data(company_data, sales_team, customers)

    # Generate Support data
    generate_support_data(company_data, customers)

    # Generate Finance data
    generate_finance_data(company_data, customers)

    # Generate Marketing data
    generate_marketing_data(company_data, customers)

    print("Data generation complete. Check the 'data' folder for output files.")

if __name__ == "__main__":
    main()