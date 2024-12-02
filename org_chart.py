# org_chart.py

import os
import pandas as pd
from chatgpt import chat_with_instructor
from docx import Document
from docx.shared import Pt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='org_chart.log')

async def generate_org_chart_async(company_data):
    # Load employee data
    df_employees = pd.read_csv(os.path.join('data', 'employees.csv'))
    simplified_employees = df_employees[['employee_id', 'first_name', 'last_name', 'title', 'department', 'manager_name', 'work_location', 'remote']]
    employees = simplified_employees.to_dict('records')

    # Prepare the prompt
    prompt = f"""
You are an HR specialist at {company_data['company_name']}. Based on the following employee data, create an organizational chart in the specified format.

Employee Data:
{employees}

Format:
[Provide the desired format here, similar to the sample organizational chart provided earlier.]

Ensure that the chart includes:
- Hierarchical structure
- Employee names and IDs
- Positions and departments
- Locations and remote status
- Reporting lines

Here is an example of the expected format:

Advanced Cloud Organizational Chart

1. Executive Leadership
Emily Smith (AC001)
* Position: Chief Executive Officer (CEO)
* Department: Executive
* Location: San Francisco, CA
* Remote: No
* Reports To: Board of Directors (AC000)


2. Direct Reports to the CEO
A. James Garcia (AC008)
* Position: Engineering Manager
* Department: R&D/Product
* Location: San Francisco, CA
* Remote: No
* Reports To: Emily Smith (AC001)
B. Michael Johnson (AC002)
* Position: Vice President of Sales
* Department: Sales
* Location: New York, NY
* Remote: No
* Reports To: Emily Smith (AC001)
C. Linda Williams (AC003)
* Position: Vice President of Support
* Department: Support
* Location: Seattle, WA
* Remote: Yes
* Reports To: Emily Smith (AC001)
D. David Brown (AC004)
* Position: Vice President of Customer Experience
* Department: Customer Experience
* Location: Austin, TX
* Remote: No
* Reports To: Emily Smith (AC001)
E. Susan Jones (AC005)
* Position: Vice President of Marketing
* Department: Marketing
* Location: Boston, MA
* Remote: No
* Reports To: Emily Smith (AC001)
...

3. Departmental Structure
A. R&D/Product Department
Led by James Garcia (AC008), Engineering Manager
Team Members:
1. Patricia Martinez (AC009)
   * Position: Software Engineer II
   * Location: San Francisco, CA
   * Remote: No
   * Reports To: James Garcia (AC008)
2. John Lopez (AC010)
   * Position: Software Engineer I
   * Location: Austin, TX
   * Remote: Yes
   * Reports To: James Garcia (AC008)
... (additional R&D team members)

B. Sales Department
Led by Michael Johnson (AC002), VP of Sales
Direct Report:
* Robert Miller (AC006)
   * Position: Sales Operations Manager
   * Location: Chicago, IL
   * Remote: Yes
   * Reports To: Michael Johnson (AC002)
Sales Team:
1. Richard Anderson (AC014)
   * Position: Account Executive
   * Location: New York, NY
   * Remote: Yes
   * Reports To: Michael Johnson (AC002)
2. Mary Thomas (AC015)
   * Position: Sales Associate
   * Location: Chicago, IL
   * Remote: No
   * Reports To: Michael Johnson (AC002)
... (additional sales team members)



C. Support Department
Led by Linda Williams (AC003), VP of Support
Team Members:
1. Daniel Martinez (AC024)
   * Position: Support Engineer
   * Location: Austin, TX
   * Remote: Yes
   * Reports To: Linda Williams (AC003)
2. Ashley Robinson (AC025)
   * Position: Support Engineer
   * Location: Seattle, WA
   * Remote: No
   * Reports To: Linda Williams (AC003)
... (additional support team members)


... (additional departmental structures)

Output the full organizational chart as plain text.
"""

    try:
        org_chart_text = await asyncio.to_thread(chat_with_instructor, prompt, str)
        if org_chart_text:
            org_chart_text = org_chart_text.strip()
            # Save org chart as text file
            with open(os.path.join('data', 'org_chart.txt'), 'w', encoding='utf-8') as f:
                f.write(org_chart_text)
            print("Organizational chart generated in 'data/org_chart.txt'.")
            logging.info("Organizational chart generated.")

            # Generate DOCX and PDF files
            generate_org_chart_docx(org_chart_text)
            generate_org_chart_pdf(org_chart_text)
        else:
            print("Failed to generate organizational chart.")
            logging.error("Failed to generate organizational chart.")
    except Exception as e:
        logging.error(f"Error generating organizational chart: {e}")
        print("Error generating organizational chart.")

def generate_org_chart(company_data):
    asyncio.run(generate_org_chart_async(company_data))

def generate_org_chart_docx(org_chart_text):
    document = Document()
    for line in org_chart_text.split('\n'):
        if line.strip() == '':
            document.add_paragraph('')
        elif line.strip().startswith('1.') or line.strip().startswith('2.') or line.strip().startswith('3.'):
            document.add_heading(line.strip(), level=1)
        elif line.strip()[0].isalpha() and line.strip()[1] == '.':
            document.add_heading(line.strip(), level=2)
        elif line.strip()[0].isdigit() and '.' in line:
            p = document.add_paragraph(line.strip())
            p.paragraph_format.left_indent = Pt(36)
        elif line.strip().startswith('*') or line.strip().startswith('-'):
            p = document.add_paragraph(line.strip())
            p.paragraph_format.left_indent = Pt(72)
        else:
            document.add_paragraph(line.strip())
    document.save(os.path.join('data', 'org_chart.docx'))
    print("Organizational chart generated in 'data/org_chart.docx'.")

def generate_org_chart_pdf(org_chart_text):
    doc = SimpleDocTemplate(
        os.path.join('data', 'org_chart.pdf'),
        pagesize=LETTER
    )
    styles = getSampleStyleSheet()
    # Use unique style names to avoid conflicts
    if 'CustomBullet' not in styles:
        styles.add(ParagraphStyle(name='CustomBullet', parent=styles['Normal'], bulletIndent=0, leftIndent=20))
    Story = []
    lines = org_chart_text.split('\n')
    for line in lines:
        line = line.strip()
        if line == '':
            Story.append(Spacer(1, 12))
        elif line.startswith('•') or line.startswith('*') or line.startswith('-'):
            Story.append(Paragraph(line[1:].strip(), styles['CustomBullet']))
        else:
            Story.append(Paragraph(line, styles['Normal']))
    doc.build(Story)
    print("Organizational chart generated in 'data/org_chart.pdf'.")

if __name__ == "__main__":
    company_data = {
        'company_name': 'Advanced Cloud'
    }
    generate_org_chart(company_data)