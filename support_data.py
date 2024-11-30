# support_data.py

import os
import pandas as pd
from faker import Faker
import random
import uuid
import asyncio
import logging
from chatgpt import chat_with_instructor

fake = Faker()
Faker.seed(0)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='support_data.log')

async def generate_issue_summary(contact_name, customer_name, company_name):
    prompt = f"""
You are a customer named {contact_name} from {customer_name} using {company_name}'s services. Describe a technical issue you are experiencing in one sentence, related to common SaaS problems like login issues, performance problems, or feature malfunctions. Avoid using any personal data or disallowed content.
"""
    try:
        issue_summary = await asyncio.to_thread(chat_with_instructor, prompt, str)
        return issue_summary.strip() if issue_summary else None
    except Exception as e:
        logging.error(f"Error generating issue summary for {customer_name}: {e}")
        return None

async def generate_support_ticket(customer, company_name, statuses):
    customer_id = customer['customer_id']
    customer_name = customer['company_name']
    contact_name = fake.name()
    issue_summary = await generate_issue_summary(contact_name, customer_name, company_name)
    if issue_summary is None:
        return None

    status = random.choice(statuses)
    tags = [fake.word() for _ in range(3)]
    kb_reference = random.choice([True, False])
    email_date = fake.date_between(start_date='-1y', end_date='today').isoformat()
    email_conversations = f"Email exchange with {contact_name} on {email_date}"

    ticket = {
        'ticket_id': f"TICK{str(uuid.uuid4())[:8]}",
        'customer_id': customer_id,
        'issue_summary': issue_summary,
        'status': status,
        'tags': tags,
        'kb_reference': kb_reference,
        'email_conversations': email_conversations
    }
    return ticket

def generate_support_data(company_data, customers, knowledge_base):
    support_tickets = []
    statuses = ['Open', 'Pending', 'Resolved', 'Closed']
    num_tickets = 200

    async def main():
        tasks = [
            generate_support_ticket(random.choice(customers), company_data['company_name'], statuses)
            for _ in range(num_tickets)
        ]
        return await asyncio.gather(*tasks)

    # Use asyncio.run() instead of get_event_loop()
    results = asyncio.run(main())

    # Filter out None results
    support_tickets = [ticket for ticket in results if ticket is not None]

    # Save to CSV
    df_tickets = pd.DataFrame(support_tickets)
    df_tickets.to_csv(os.path.join('data', 'support_tickets.csv'), index=False)

    logging.info("Support data generated.")
    print("Support data generated.")
    return support_tickets