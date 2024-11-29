# company_info.py

import os
import json
from pydantic import BaseModel, Field
from chatgpt import chat_with_instructor
import utils

# Define the Pydantic model for Company Information
class CompanyInfo(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    description: str = Field(..., description="Description of the company")
    products: list = Field(..., description="List of products offered")
    mission: str = Field(..., description="Company's mission statement")
    vision: str = Field(..., description="Company's vision statement")
    cash_at_bank: float = Field(..., description="Amount of cash at bank in USD")

def generate_company_info():
    prompt = """
    Create a fictional SaaS B2B company with the following details:
    - A 4-year-old business specializing in cloud infrastructure.
    - List 5 products they offer.
    - Describe the company's mission and vision.
    - Mention that they have $6M cash at bank.
    Provide this information in JSON format matching the following schema:

    {
        "company_name": "string",
        "description": "string",
        "products": ["string"],
        "mission": "string",
        "vision": "string",
        "cash_at_bank": float
    }
    """

    # Use chat_with_instructor to get the company information
    company_data = chat_with_instructor(prompt, response_model=CompanyInfo)

    # Convert to dictionary
    company_dict = company_data.model_dump()
    

    # Save to a JSON file
    with open(os.path.join('data', 'company_info.json'), 'w') as f:
        json.dump(company_dict, f, indent=4)

    print("Company information generated.")

    # Update shared data
    utils.company_data = company_dict

    return company_dict