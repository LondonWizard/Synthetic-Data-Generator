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
    employees = df_employees.to_dict('records')

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

Output the organizational chart as plain text.
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