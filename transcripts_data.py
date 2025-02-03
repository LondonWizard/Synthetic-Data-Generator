# transcripts_data.py

import os
import asyncio
from chatgpt import chat_with_instructor

# Create the transcripts_data folder if it doesn't exist
if not os.path.exists('transcripts_data'):
    os.makedirs('transcripts_data')

# Define 10 different organization types
ORGANIZATION_TYPES = [
    "SaaS",
    "Healthcare",
    "Real_Estate",
    "Finance",
    "Education",
    "Retail",
    "Government_Agency",
    "Manufacturing",
    "Non_Profit",
    "Law_Firm"
]

async def generate_one_transcript(org_type: str) -> str:
    """
    Generates a single meeting transcript for a given organization type
    by calling the `chat_with_instructor` function from chatgpt.py.
    """
    prompt = f"""
You are a creative and professional meeting scribe. 
Generate a realistic and well-structured meeting transcript for a one-hour meeting 
in a {org_type} organization. 

Meeting Requirements:
1. The transcript should include:
   - Date and Time of the meeting.
   - Meeting topic relevant to a {org_type} context.
   - A list of participants with their roles (e.g., manager, director, specialist).
   - Timestamps and short speaker labels before each statement.
   - At least one minor conflict or disagreement that gets resolved or tabled.
   - Clear action items or next steps.

2. The tone should mostly be professional and the transcript should follow a format 
   similar to your previously provided example. However, in each transcript, there should be a small percentage of members who deviate from the professional tone and show negative behaviors, such as dismissive tone, lack of teamwork, etc. Overall, there should be imperfections in each candidate, with their own strengths and weaknesses clearly present in their participation.

3. Keep the transcript around 1–2 pages (a few hundred words), 
   avoiding personal data or disallowed content.

Provide the transcript in plain text.
"""
    try:
        # Call the chat_with_instructor function
        response = chat_with_instructor(prompt, str)
        return response
    except Exception as e:
        return f"Error generating transcript for {org_type}: {e}"

async def generate_transcripts():
    """
    Asynchronously generates 10 different transcripts for each organization type
    and saves them to the `transcripts_data` folder.
    """
    tasks = []
    for org_type in ORGANIZATION_TYPES:
        tasks.append(generate_one_transcript(org_type))

    transcripts = await asyncio.gather(*tasks)

    # Save each transcript in a separate file
    for org_type, transcript in zip(ORGANIZATION_TYPES, transcripts):
        filename = f"transcripts_data/{org_type}_meeting_transcript.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"Transcript for {org_type} saved to {filename}.")

def main():
    # Run the event loop to generate transcripts
    asyncio.run(generate_transcripts())
    print("All transcripts generated.")

if __name__ == "__main__":
    main()