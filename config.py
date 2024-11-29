#/config.py/

import os
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI
from instructor import from_openai, Mode
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") # Get the API key from the environment

# Define the configuration settings for OpenAI API
client = OpenAI(
  api_key=OPENAI_API_KEY
)
# Define the configuration settings for the instructor library
instructor_client = from_openai(client)

def get_openai_client():
  return client

def get_instructor_client():
    return instructor_client