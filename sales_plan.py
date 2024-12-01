# sales_plan.py

import os
import pandas as pd
from pydantic import BaseModel, Field
from typing import List
from chatgpt import chat_with_instructor
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='sales_plan.log')

class SalesTarget(BaseModel):
    sales_rep_id: str = Field(..., description="Employee ID of the sales representative.")
    sales_rep_name: str = Field(..., description="Full name of the sales representative.")
    role: str = Field(..., description="Role of the sales representative (e.g., Account Executive, Sales Associate).")
    location: str = Field(..., description="Work location of the sales representative.")
    reports_to: str = Field(..., description="Manager's name.")
    total_sales_target: float = Field(..., description="Total sales target assigned to the representative.")
    new_sales_target: float = Field(..., description="Target for new sales (new clients).")
    upsell_target: float = Field(..., description="Target for upsells (existing clients).")
    strategies: List[str] = Field(..., description="Strategies for achieving the targets.")
    assigned_sales_associates: List[str] = Field(..., description="List of assigned Sales Associates (if any).")

class SalesPlan(BaseModel):
    company_name: str = Field(..., description="Name of the company.")
    total_revenue_target: float = Field(..., description="Total revenue target for the year.")
    new_sales_target: float = Field(..., description="Revenue target from new clients.")
    upsell_target: float = Field(..., description="Revenue target from existing clients.")
    sales_team_structure: List[dict] = Field(..., description="Structure of the sales team.")
    sales_targets: List[SalesTarget] = Field(..., description="Sales targets for each team member.")
    vp_responsibilities: List[str] = Field(..., description="Responsibilities of the VP of Sales.")
    action_plan: List[str] = Field(..., description="Strategies and action plans.")
    expected_outcomes: List[str] = Field(..., description="Expected outcomes from the plan.")
    contingency_plans: List[str] = Field(..., description="Contingency plans.")

async def generate_sales_plan_async(company_data):
    # Load data
    df_employees = pd.read_csv(os.path.join('data', 'employees.csv'))
    df_targets = pd.read_csv(os.path.join('data', 'sales_targets.csv'))

    # Prepare sales plan data
    sales_team_structure = []
    sales_targets = []
    total_revenue_target = 10000000
    new_sales_target = 6000000
    upsell_target = 4000000

    # Build sales team structure and sales targets
    for _, emp in df_employees.iterrows():
        if emp['department'] == 'Sales':
            role = emp['title']
            manager_name = emp['manager_name']
            sales_team_structure.append({
                'name': f"{emp['first_name']} {emp['last_name']} ({emp['employee_id']})",
                'position': role,
                'location': emp['work_location'],
                'reports_to': manager_name
            })

            # Get sales targets if available
            target_row = df_targets[df_targets['sales_rep_id'] == emp['employee_id']]
            if not target_row.empty:
                target_row = target_row.iloc[0]
                sales_target = SalesTarget(
                    sales_rep_id=emp['employee_id'],
                    sales_rep_name=f"{emp['first_name']} {emp['last_name']}",
                    role=role,
                    location=emp['work_location'],
                    reports_to=manager_name,
                    total_sales_target=target_row['total_sales_target'],
                    new_sales_target=target_row['new_clients_target'],
                    upsell_target=target_row['existing_clients_target'],
                    strategies=["Custom strategies will be included here."],
                    assigned_sales_associates=[]
                )
                sales_targets.append(sales_target)

    # Create sales plan object
    sales_plan_data = SalesPlan(
        company_name=company_data['company_name'],
        total_revenue_target=total_revenue_target,
        new_sales_target=new_sales_target,
        upsell_target=upsell_target,
        sales_team_structure=sales_team_structure,
        sales_targets=sales_targets,
        vp_responsibilities=[
            "Overall Accountability: Ensure the sales team meets the $10 million revenue target.",
            "Strategic Planning: Adjust strategies as needed.",
            "Team Support: Conduct performance reviews and foster collaboration."
        ],
        action_plan=[
            "Enhanced Collaboration",
            "Training and Development",
            "Market Segmentation",
            "Performance Incentives",
            "Resource Support"
        ],
        expected_outcomes=[
            "Revenue Achievement",
            "Increased Productivity",
            "Professional Growth",
            "Market Penetration"
        ],
        contingency_plans=[
            "Underperformance: Implement coaching plans.",
            "Resource Shifts: Reallocate resources as needed.",
            "Market Changes: Adjust strategies based on feedback."
        ]
    )

    # Prepare the prompt
    prompt = f"""
You are the Vice President of Sales at {sales_plan_data.company_name}. Based on the following sales plan data, create a comprehensive sales plan matching the format of the provided example.

Sales Plan Data:
{sales_plan_data.json()}

Ensure the sales plan includes:
- Introduction
- Sales Team Structure
- Sales Targets
- Calculating Individual Targets
- Individual Sales Plans
- VP of Sales Responsibilities
- Action Plan and Strategies
- Expected Outcomes
- Contingency Plans
- Conclusion

Use headings, subheadings, bullet points, and numbering where appropriate. Output the sales plan as plain text, formatted appropriately.
"""

    try:
        sales_plan_text = await asyncio.to_thread(chat_with_instructor, prompt, str)
        if sales_plan_text:
            sales_plan_text = sales_plan_text.strip()
            # Save sales plan as text file
            with open(os.path.join('data', 'sales_plan.txt'), 'w', encoding='utf-8') as f:
                f.write(sales_plan_text)
            print("Sales plan generated in 'data/sales_plan.txt'.")
            logging.info("Sales plan generated.")

            # Generate DOCX and PDF files
            generate_sales_plan_docx(sales_plan_text)
            generate_sales_plan_pdf(sales_plan_text)
        else:
            print("Failed to generate sales plan.")
            logging.error("Failed to generate sales plan.")
    except Exception as e:
        logging.error(f"Error generating sales plan: {e}")
        print("Error generating sales plan.")

def generate_sales_plan(company_data):
    asyncio.run(generate_sales_plan_async(company_data))

def generate_sales_plan_docx(sales_plan_text):
    document = Document()
    styles = document.styles

    # Modify styles for better formatting
    heading_style = styles['Heading 1']
    heading_style.font.name = 'Arial'
    heading_style.font.size = Pt(16)

    normal_style = styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(11)

    lines = sales_plan_text.split('\n')
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        elif line.endswith("(Revised)"):
            document.add_heading(line, level=0)
        elif line in [
            "Introduction", "Sales Team Structure", "Sales Targets",
            "Calculating Individual Targets", "Individual Sales Plans",
            "VP of Sales Responsibilities", "Action Plan and Strategies",
            "Expected Outcomes", "Contingency Plans", "Conclusion"
        ]:
            document.add_heading(line, level=1)
        elif line.startswith('*') or line.startswith('•') or line.startswith('-'):
            p = document.add_paragraph(line[1:].strip(), style='List Bullet')
        elif line[0].isdigit() and (line[1] == '.' or line[1] == ')'):
            p = document.add_paragraph(line, style='List Number')
        else:
            document.add_paragraph(line)
    document.save(os.path.join('data', 'sales_plan.docx'))
    print("Sales plan generated in 'data/sales_plan.docx'.")

def generate_sales_plan_pdf(sales_plan_text):
    doc = SimpleDocTemplate(
        os.path.join('data', 'sales_plan.pdf'),
        pagesize=LETTER
    )
    styles = getSampleStyleSheet()
    # Use unique style names to avoid conflicts
    if 'CustomBullet' not in styles:
        styles.add(ParagraphStyle(name='CustomBullet', parent=styles['Normal'], bulletIndent=0, leftIndent=20))
    if 'CustomNumber' not in styles:
        styles.add(ParagraphStyle(name='CustomNumber', parent=styles['Normal'], bulletIndent=0, leftIndent=20))
    Story = []
    lines = sales_plan_text.split('\n')
    for line in lines:
        line = line.strip()
        if line == '':
            Story.append(Spacer(1, 12))
        elif line.endswith("(Revised)"):
            Story.append(Paragraph(line, styles['Title']))
        elif line in [
            "Introduction", "Sales Team Structure", "Sales Targets",
            "Calculating Individual Targets", "Individual Sales Plans",
            "VP of Sales Responsibilities", "Action Plan and Strategies",
            "Expected Outcomes", "Contingency Plans", "Conclusion"
        ]:
            Story.append(Paragraph(line, styles['Heading1']))
        elif line.startswith('*') or line.startswith('•') or line.startswith('-'):
            Story.append(Paragraph(line[1:].strip(), styles['CustomBullet']))
        elif line[0].isdigit() and (line[1] == '.' or line[1] == ')'):
            Story.append(Paragraph(line, styles['CustomNumber']))
        else:
            Story.append(Paragraph(line, styles['Normal']))
    doc.build(Story)
    print("Sales plan generated in 'data/sales_plan.pdf'.")

if __name__ == "__main__":
    company_data = {
        'company_name': 'Advanced Cloud'
    }
    generate_sales_plan(company_data)