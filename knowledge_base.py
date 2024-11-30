# knowledge_base.py

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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='knowledge_base.log')

async def generate_article(topic, company_name):
    prompt = f"""
You are creating a knowledge base article for {company_name}. Write a comprehensive article on '{topic}', including step-by-step instructions, best practices, and helpful tips. Ensure the content is clear, professional, and free of disallowed content.
"""
    try:
        content = await asyncio.to_thread(chat_with_instructor, prompt, str)
        return content.strip() if content else None
    except Exception as e:
        logging.error(f"Error generating knowledge base article on {topic}: {e}")
        return None

def generate_knowledge_base(company_data):
    articles = []
    topics = ['Getting Started', 'Account Management', 'Billing', 'Troubleshooting', 'Advanced Features']
    num_articles = 50

    async def main():
        tasks = []
        for _ in range(num_articles):
            topic = random.choice(topics)
            article_id = f"KB{str(uuid.uuid4())[:8]}"
            task = generate_article(topic, company_data['company_name'])
            tasks.append((article_id, topic, task))
        results = await asyncio.gather(*[task for _, _, task in tasks])
        return [(article_id, topic, content) for (article_id, topic, _), content in zip(tasks, results)]

    # Use asyncio.run() instead of get_event_loop()
    results = asyncio.run(main())

    for article_id, topic, content in results:
        if content:
            article = {
                'article_id': article_id,
                'topic': topic,
                'title': f"{topic} Guide",
                'content': content
            }
            articles.append(article)

    # Save to CSV
    df_articles = pd.DataFrame(articles)
    df_articles.to_csv(os.path.join('data', 'knowledge_base.csv'), index=False)

    logging.info("Knowledge base generated.")
    print("Knowledge base generated.")
    return articles