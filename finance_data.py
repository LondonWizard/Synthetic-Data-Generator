# finance_data.py

import os
import pandas as pd
from pydantic import BaseModel, Field
from faker import Faker
import random
from datetime import timedelta, datetime
import utils

fake = Faker()
Faker.seed(0)

class Invoice(BaseModel):
    invoice_id: str = Field(..., description="Unique identifier for the invoice")
    customer_id: str = Field(..., description="Customer ID")
    amount: float = Field(..., description="Invoice amount")
    currency: str = Field(..., description="Currency of the invoice")
    issue_date: str = Field(..., description="Date the invoice was issued")
    due_date: str = Field(..., description="Due date for the invoice")
    paid: bool = Field(..., description="Whether the invoice has been paid")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")
    fx_difference: float = Field(..., description="Difference due to currency exchange rates")

def generate_finance_data(company_data, customers):
    currencies = ['USD', 'EUR', 'GBP', 'MXN']
    invoices = []

    for customer in customers:
        num_invoices = random.randint(1, 5)
        for _ in range(num_invoices):
            amount = round(random.uniform(20_000, 250_000), 2)
            currency = random.choices(currencies, weights=[60, 15, 15, 10], k=1)[0]
            issue_date = fake.date_between(start_date='-1y', end_date='today')
            due_date = issue_date + timedelta(days=30)
            paid = fake.boolean(chance_of_getting_true=70)
            transaction_amount = amount if paid else 0.0
            transaction_date = issue_date + timedelta(days=random.randint(0, 60)) if paid else None
            fx_difference = 0.0

            if currency != 'USD':
                fx_rate = random.uniform(0.8, 1.2)  # Simulate FX rate fluctuation
                transaction_amount = round(amount * fx_rate, 2)
                fx_difference = round(transaction_amount - amount, 2)

            invoice = Invoice(
                invoice_id=f"INV{fake.uuid4()}",
                customer_id=customer['customer_id'],
                amount=amount,
                currency=currency,
                issue_date=issue_date.isoformat(),
                due_date=due_date.isoformat(),
                paid=paid,
                transaction_amount=transaction_amount,
                transaction_date=transaction_date.isoformat() if transaction_date else None,
                fx_difference=fx_difference
            )
            invoices.append(invoice.dict())

    # Save to CSV
    df = pd.DataFrame(invoices)
    df.to_csv(os.path.join('data', 'invoices.csv'), index=False)

    # Generate 13-Week Cash Forecast
    cash_forecast = []
    starting_cash = 6_000_000  # As per company data
    for week in range(1, 14):
        inflow = sum([inv['transaction_amount'] for inv in invoices if inv['transaction_date'] and
                      datetime.fromisoformat(inv['transaction_date']).isocalendar()[1] == week])
        outflow = random.uniform(50_000, 150_000)  # Simulate expenses
        ending_cash = starting_cash + inflow - outflow
        cash_forecast.append({
            'week': week,
            'starting_cash': starting_cash,
            'inflow': inflow,
            'outflow': outflow,
            'ending_cash': ending_cash
        })
        starting_cash = ending_cash

    df_forecast = pd.DataFrame(cash_forecast)
    df_forecast.to_csv(os.path.join('data', 'cash_forecast.csv'), index=False)

    # Generate MRR File (Monthly Recurring Revenue)
    mrr_data = []
    for month in range(1, 13):
        mrr = sum([inv['amount'] for inv in invoices if inv['issue_date'] and
                   datetime.fromisoformat(inv['issue_date']).month == month]) / 12
        mrr_data.append({
            'month': month,
            'mrr': mrr
        })

    df_mrr = pd.DataFrame(mrr_data)
    df_mrr.to_csv(os.path.join('data', 'mrr.csv'), index=False)

    print("Finance data generated.")