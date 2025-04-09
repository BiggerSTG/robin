from  openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def query_llm(prompt):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    raw_output = response.choices[0].message.content
    return raw_output