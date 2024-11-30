# marketing_data.py

import os
import pandas as pd
from faker import Faker
import random
import uuid
import asyncio
import logging
from datetime import datetime, timedelta
from chatgpt import chat_with_instructor

fake = Faker()
Faker.seed(0)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='marketing_data.log')

async def generate_brandbook(company_data):
    prompt = f"""
You are a brand strategist tasked with creating a brandbook for {company_data['company_name']}. The brandbook should include the company's mission, vision, core values, brand voice, visual guidelines, and messaging framework. Ensure the content is professional and aligns with a SaaS cloud service provider.
"""
    try:
        brandbook_content = await asyncio.to_thread(chat_with_instructor, prompt, str)
        return brandbook_content.strip() if brandbook_content else None
    except Exception as e:
        logging.error(f"Error generating brandbook: {e}")
        return None

def generate_marketing_data(company_data, customers):
    campaigns = []
    leads = []
    num_campaigns = 20

    for _ in range(num_campaigns):
        campaign_id = f"CMP{str(uuid.uuid4())[:8]}"
        campaign_name = f"{fake.bs().title()} Campaign"
        start_date = fake.date_between(start_date='-6m', end_date='-3m')
        end_date = start_date + timedelta(days=random.randint(30, 90))
        budget = round(random.uniform(10000, 50000), 2)

        campaign = {
            'campaign_id': campaign_id,
            'campaign_name': campaign_name,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'budget': budget
        }
        campaigns.append(campaign)

        # Generate leads for the campaign
        num_leads = random.randint(50, 200)
        for _ in range(num_leads):
            lead_id = f"LEAD{str(uuid.uuid4())[:8]}"
            lead_name = fake.name()
            company = fake.company()
            email = fake.email()
            phone = fake.phone_number()
            status = random.choice(['New', 'Contacted', 'Qualified', 'Converted'])

            lead = {
                'lead_id': lead_id,
                'campaign_id': campaign_id,
                'lead_name': lead_name,
                'company': company,
                'email': email,
                'phone': phone,
                'status': status
            }
            leads.append(lead)

    # Save campaigns to CSV
    df_campaigns = pd.DataFrame(campaigns)
    df_campaigns.to_csv(os.path.join('data', 'campaigns.csv'), index=False)

    # Save leads to CSV
    df_leads = pd.DataFrame(leads)
    df_leads.to_csv(os.path.join('data', 'leads.csv'), index=False)

    # Generate brandbook asynchronously
    async def main():
        brandbook_content = await generate_brandbook(company_data)
        return brandbook_content

    # Use asyncio.run() instead of get_event_loop()
    brandbook_content = asyncio.run(main())

    # Save brandbook to a text file
    if brandbook_content:
        with open(os.path.join('data', 'brandbook.txt'), 'w') as f:
            f.write(brandbook_content)
        logging.info("Brandbook generated.")
        print("Brandbook generated.")
    else:
        logging.error("Brandbook generation failed.")
        print("Brandbook generation failed.")

    logging.info("Marketing data generated.")
    print("Marketing data generated.")
    return campaigns, leads