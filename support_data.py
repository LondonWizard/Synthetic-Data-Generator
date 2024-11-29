# support_data.py

import os
import pandas as pd
from pydantic import BaseModel, Field
from faker import Faker
import utils
import random

fake = Faker()
Faker.seed(0)

class SupportTicket(BaseModel):
    ticket_id: str = Field(..., description="Unique identifier for the support ticket")
    customer_id: str = Field(..., description="Customer ID")
    issue_summary: str = Field(..., description="Summary of the issue")
    status: str = Field(..., description="Current status of the ticket")
    tags: list = Field(..., description="Tags associated with the ticket")
    kb_reference: bool = Field(..., description="Whether the issue is covered in the knowledge base")
    email_conversations: str = Field(..., description="Summary of email conversations")

def generate_support_data(company_data, customers):
    statuses = ['Open', 'Pending', 'Resolved', 'Closed']
    tickets = []

    for _ in range(200):
        customer = random.choice(customers)
        ticket = SupportTicket(
            ticket_id=f"TICK{fake.uuid4()}",
            customer_id=customer['customer_id'],
            issue_summary=fake.sentence(nb_words=6),
            status=random.choice(statuses),
            tags=fake.words(nb=3),
            kb_reference=fake.boolean(chance_of_getting_true=70),
            email_conversations=f"Email exchange with {fake.name()} on {fake.date_this_year().isoformat()}"
        )
        tickets.append(ticket.dict())

    # Save to CSV
    df = pd.DataFrame(tickets)
    df.to_csv(os.path.join('data', 'support_tickets.csv'), index=False)

    # Generate Knowledge Base Articles
    kb_articles = []
    for i in range(1, 51):
        article = {
            "article_id": f"KB{str(i).zfill(4)}",
            "title": fake.sentence(nb_words=6),
            "content": fake.paragraph(nb_sentences=5),
            "tags": fake.words(nb=3)
        }
        kb_articles.append(article)
    df_kb = pd.DataFrame(kb_articles)
    df_kb.to_csv(os.path.join('data', 'knowledge_base.csv'), index=False)

    print("Support data generated.")