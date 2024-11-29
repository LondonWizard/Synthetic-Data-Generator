#/chatgpt.py/

import config
import openai
from pydantic import BaseModel

# Define the chat function
def chat(prompt):
  # Get the OpenAI client
  client = config.get_openai_client()
  # Call the OpenAI API
  completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
              {"role": "user", "content": prompt},
            ]
        )
  return completion.choices[0].message.content

def chat_with_instructor(prompt, response_model: BaseModel):
  # Get the instructor client
  client = config.get_instructor_client()
  # Call the instructor API
  completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt},
        ],
        response_model=response_model,
        max_retries=8
        )
  return completion
