# main.py

import os
import argparse
from company_info import generate_company_info
from hr_data import generate_hr_data
import sales_data
from crm_data import generate_crm_data
from support_data import generate_support_data
from finance_data import generate_finance_data
from marketing_data import generate_marketing_data
from knowledge_base import generate_knowledge_base
from sales_targets import generate_sales_targets
import org_chart
import sales_plan
import ae_handbook

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Synthetic Data Generator')
    parser.add_argument('--employee_count', type=int, default=200, help='Number of employees to generate')
    # Removed --account_executive_count as it's now calculated based on employee_count and sales proportion
    parser.add_argument('--num_opportunities', type=int, default=200, help='Number of sales opportunities')
    parser.add_argument('--total_sales_target', type=float, default=10000000, help='Total sales target')
    parser.add_argument('--new_clients_percentage', type=float, default=60.0, help='Percentage of sales target from new clients')
    parser.add_argument('--international_clients_percentage', type=float, default=30.0, help='Percentage of international clients')
    args = parser.parse_args()

    # Create the data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Generate Company Info
    company_data = generate_company_info()

    # Generate HR data
    employees = generate_hr_data(company_data, args.employee_count)

    # Generate Sales data
    customers, sales_team, opportunities = sales_data.generate_sales_data(
        company_data, employees, args.num_opportunities
    )

    # Generate Sales Targets
    generate_sales_targets(sales_team, args.total_sales_target, args.new_clients_percentage)

    # Generate CRM data
    generate_crm_data(company_data, sales_team, customers)

    # Generate Knowledge Base
    knowledge_base = generate_knowledge_base(company_data)

    # Generate Support data
    generate_support_data(company_data, customers, knowledge_base)

    # Generate Finance data
    generate_finance_data(company_data, customers, args.international_clients_percentage)

    # Generate Marketing data
    generate_marketing_data(company_data, customers)

    # Generate Organizational Chart
    org_chart.generate_org_chart(company_data)

    # Generate Sales Plan
    sales_plan.generate_sales_plan(company_data)

    # Generate Account Executive Handbook
    ae_handbook.generate_ae_handbook(company_data)

    print("Data generation complete. Check the 'data' folder for output files.")

if __name__ == "__main__":
    main()