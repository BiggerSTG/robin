from  openai import OpenAI
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def query_llm(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    raw_output = response.choices[0].message.content
    return raw_output

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GEMINI_API_KEY")

def query_llm_gemini(prompt, system_instruction=None):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-03-25",
        contents=prompt
    )
    return response.text