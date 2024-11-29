# marketing_data.py

import os
import pandas as pd
from pydantic import BaseModel, Field
from faker import Faker
import random
import utils
from datetime import timedelta, datetime

fake = Faker()
Faker.seed(0)

class Lead(BaseModel):
    lead_id: str = Field(..., description="Unique identifier for the lead")
    name: str = Field(..., description="Name of the lead")
    email: str = Field(..., description="Email of the lead")
    source: str = Field(..., description="Source channel of the lead")
    campaign: str = Field(..., description="Marketing campaign associated")
    ad_text: str = Field(..., description="Text of the ad clicked")
    website_visits: int = Field(..., description="Number of website visits")
    conversion: bool = Field(..., description="Whether the lead converted")

def generate_marketing_data(company_data, customers):
    sources = ['Google Ads', 'Facebook Ads', 'LinkedIn', 'Organic Search', 'Referral']
    campaigns = ['Spring Sale', 'Summer Promo', 'Fall Discount', 'Winter Offer']
    leads = []

    for _ in range(500):
        lead = Lead(
            lead_id=f"LEAD{fake.uuid4()}",
            name=fake.name(),
            email=fake.email(),
            source=random.choice(sources),
            campaign=random.choice(campaigns),
            ad_text=fake.sentence(nb_words=6),
            website_visits=random.randint(1, 10),
            conversion=fake.boolean(chance_of_getting_true=30)
        )
        leads.append(lead.dict())

    # Save to CSV
    df = pd.DataFrame(leads)
    df.to_csv(os.path.join('data', 'leads.csv'), index=False)

    # Generate Ads Data
    ads_data = []
    for source in sources:
        for campaign in campaigns:
            ad = {
                'ad_id': f"AD{fake.uuid4()}",
                'source': source,
                'campaign': campaign,
                'impressions': random.randint(1000, 10000),
                'clicks': random.randint(100, 1000),
                'ctr': round(random.uniform(1.0, 10.0), 2),
                'cost': round(random.uniform(500.0, 5000.0), 2)
            }
            ads_data.append(ad)

    df_ads = pd.DataFrame(ads_data)
    df_ads.to_csv(os.path.join('data', 'ads_data.csv'), index=False)

    # Generate Google Analytics Data
    ga_data = []
    for day in range(1, 31):
        ga = {
            'date': (datetime.now() - timedelta(days=day)).isoformat(),
            'page_views': random.randint(1000, 5000),
            'unique_visitors': random.randint(500, 2500),
            'bounce_rate': round(random.uniform(30.0, 70.0), 2)
        }
        ga_data.append(ga)

    df_ga = pd.DataFrame(ga_data)
    df_ga.to_csv(os.path.join('data', 'google_analytics.csv'), index=False)

    # Generate Brand Book (Placeholder)
    brand_book = "Brand guidelines content goes here."
    with open(os.path.join('data', 'brand_book.txt'), 'w') as f:
        f.write(brand_book)

    print("Marketing data generated.")