# crm_data.py

import os
import pandas as pd
from pydantic import BaseModel, Field
from faker import Faker
from datetime import datetime, timedelta
import utils
import random

fake = Faker()
Faker.seed(0)

class CRMOpportunity(BaseModel):
    opportunity_id: str = Field(..., description="Unique identifier for the opportunity")
    sales_rep_id: str = Field(..., description="Employee ID of the sales representative")
    client_name: str = Field(..., description="Name of the client")
    stage: str = Field(..., description="Current stage of the opportunity")
    amount: float = Field(..., description="Potential deal amount")
    close_date: str = Field(..., description="Expected close date")
    renewal_date: str = Field(..., description="Renewal date if applicable")
    email_conversations: str = Field(..., description="Summary of email conversations")

def generate_crm_data(company_data, sales_team, customers):
    stages = ['Discovery', 'Demo Conducted', 'Case Evaluation', 'ROI', 'Proposal', 'Legal', 'Closed Won', 'Closed Lost']
    opportunities = []

    # Generate opportunities based on sales targets
    for sales_person in sales_team:
        num_opportunities = random.randint(5, 15)
        for _ in range(num_opportunities):
            amount = round(random.normalvariate(100_000, 30_000), 2)
            amount = max(50_000, min(amount, 150_000))  # Ensure amount is between $50k and $150k

            opp = CRMOpportunity(
                opportunity_id=f"OPP{fake.uuid4()}",
                sales_rep_id=sales_person['employee_id'],
                client_name=fake.company(),
                stage=random.choice(stages),
                amount=amount,
                close_date=(datetime.now() + timedelta(days=random.randint(30, 180))).isoformat(),
                renewal_date=(datetime.now() + timedelta(days=365)).isoformat(),
                email_conversations=f"Email thread with {fake.name()} on {fake.date_this_year().isoformat()}"
            )
            opportunities.append(opp.dict())

    # Save to CSV
    df = pd.DataFrame(opportunities)
    df.to_csv(os.path.join('data', 'crm_opportunities.csv'), index=False)

    print("CRM data generated.")