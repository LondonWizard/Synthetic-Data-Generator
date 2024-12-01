# ae_handbook.py

import os
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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='ae_handbook.log')

class AEHandbook(BaseModel):
    company_name: str = Field(..., description="The name of the company.")
    last_updated: str = Field(..., description="The last updated date of the handbook.")
    sections: List[str] = Field(..., description="List of section titles to include in the handbook.")

async def generate_ae_handbook_async(company_data):
    # Prepare the handbook data
    last_updated = '11.24.2023'
    sections = [
        'Introduction',
        'Company Overview',
        'Daily Workflow Overview',
        'Managing Leads',
        'Deal Management',
        'Opportunity Management',
        'Follow-Up Communication',
        'Setting and Achieving Close Targets',
        'Time Management and Productivity',
        'Utilizing Sales Tools and CRM Systems',
        'Best Practices and Professional Development',
        'Frequently Asked Questions',
        'Appendices',
        'Resources',
        'Contact Information'
    ]

    ae_handbook_data = AEHandbook(
        company_name=company_data['company_name'],
        last_updated=last_updated,
        sections=sections
    )

    # Prepare the prompt
    prompt = f"""
You are tasked with creating an Account Executive Handbook for {ae_handbook_data.company_name}. The handbook should be comprehensive and match the following format:

Advanced Cloud
Account Executive Handbook
Last updated: {ae_handbook_data.last_updated}

[Section Titles and Content]

Ensure that each section provides detailed guidance tailored to {ae_handbook_data.company_name}'s policies and procedures. Use headings, subheadings, bullet points, and numbering where appropriate to enhance readability.

Sections to include:
{ae_handbook_data.sections}

Output the handbook as plain text, formatted appropriately.
"""

    try:
        handbook_text = await asyncio.to_thread(chat_with_instructor, prompt, str)
        if handbook_text:
            handbook_text = handbook_text.strip()
            # Save as DOCX and PDF
            generate_handbook_docx(handbook_text, ae_handbook_data)
            generate_handbook_pdf(handbook_text, ae_handbook_data)
            print("Account Executive Handbook generated.")
            logging.info("Account Executive Handbook generated.")
        else:
            print("Failed to generate Account Executive Handbook.")
            logging.error("Failed to generate Account Executive Handbook.")
    except Exception as e:
        logging.error(f"Error generating Account Executive Handbook: {e}")
        print("Error generating Account Executive Handbook.")

def generate_ae_handbook(company_data):
    asyncio.run(generate_ae_handbook_async(company_data))

def generate_handbook_docx(handbook_text, ae_handbook_data):
    document = Document()
    styles = document.styles

    # Modify styles for better formatting
    heading_style = styles['Heading 1']
    heading_style.font.name = 'Arial'
    heading_style.font.size = Pt(16)

    normal_style = styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(11)

    lines = handbook_text.split('\n')
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        elif line == ae_handbook_data.company_name or line == 'Account Executive Handbook':
            continue  # Already added
        elif line.startswith('Last updated:'):
            continue  # Already added
        elif line in ae_handbook_data.sections:
            document.add_heading(line, level=2)
        elif line.startswith('•') or line.startswith('*') or line.startswith('-'):
            p = document.add_paragraph(line[1:].strip(), style='List Bullet')
        elif line[0].isdigit() and (line[1] == '.' or line[1] == ')'):
            p = document.add_paragraph(line, style='List Number')
        else:
            document.add_paragraph(line)
    document.save(os.path.join('data', 'ae_handbook.docx'))
    print("Account Executive Handbook generated in 'data/ae_handbook.docx'.")

def generate_handbook_pdf(handbook_text, ae_handbook_data):
    doc = SimpleDocTemplate(
        os.path.join('data', 'ae_handbook.pdf'),
        pagesize=LETTER
    )
    styles = getSampleStyleSheet()
    # Use unique style names to avoid conflicts
    if 'CustomBullet' not in styles:
        styles.add(ParagraphStyle(name='CustomBullet', parent=styles['Normal'], bulletIndent=0, leftIndent=20))
    if 'CustomNumber' not in styles:
        styles.add(ParagraphStyle(name='CustomNumber', parent=styles['Normal'], bulletIndent=0, leftIndent=20))
    Story = []
    Story.append(Paragraph(ae_handbook_data.company_name, styles['Title']))
    Story.append(Paragraph('Account Executive Handbook', styles['Title']))
    Story.append(Paragraph(f"Last updated: {ae_handbook_data.last_updated}", styles['Normal']))
    Story.append(Spacer(1, 12))

    lines = handbook_text.split('\n')
    for line in lines:
        line = line.strip()
        if line == '':
            Story.append(Spacer(1, 12))
        elif line == ae_handbook_data.company_name or line == 'Account Executive Handbook':
            continue  # Already added
        elif line.startswith('Last updated:'):
            continue  # Already added
        elif line in ae_handbook_data.sections:
            Story.append(Paragraph(line, styles['Heading1']))
        elif line.startswith('•') or line.startswith('*') or line.startswith('-'):
            Story.append(Paragraph(line[1:].strip(), styles['CustomBullet']))
        elif line[0].isdigit() and (line[1] == '.' or line[1] == ')'):
            Story.append(Paragraph(line, styles['CustomNumber']))
        else:
            Story.append(Paragraph(line, styles['Normal']))
    doc.build(Story)
    print("Account Executive Handbook generated in 'data/ae_handbook.pdf'.")

if __name__ == "__main__":
    company_data = {
        'company_name': 'Advanced Cloud'
    }
    generate_ae_handbook(company_data)